#%% Libs
import pandas as pd
import io
import numpy as np
from tqdm import tqdm
from ConnLib import Connector
import argparse

#%%Parser commands
parser = argparse.ArgumentParser(description="""This code extracts hourly data from the ECCC historical weather database""")
parser.add_argument('-cfg', '--config', default='Config-dev.json',
                      help= 'Leave blank unless for testing with Dev',
                      type= str)
parser.add_argument('-ids', '--building_ids', default='sample-bldg-ids.csv',
                      help= 'Leave blank unless for testing with Dev',
                      type= str)
parser.add_argument('-mt_upd','--met_update', default = 'True', 
                      help = 'Change to false if updated metadata already exists in a pickle file', 
                      type = str)
#Parse arguments 
args = parser.parse_args()
config_file = args.config
bld_ids = args.building_ids
meta_update = args.met_update

#%% Program body
wmo_id = 71296 #This is the WMO ID field in the ECCC site
upperYearRange = 2023
lowerYearRange = 2022

# Dateranges
yearRanges = np.arange(lowerYearRange,upperYearRange,1)
monthRanges = np.arange(1,13,1)

#!The api returns day 1 to end of month regardless of the day parameter passed. 
#! No clue why. For now day has been auto set to 31, and you can pass a day if 
#! you want. However, my testing shows that it's kind of useless

#Grab the list of station IDs from the wmo_id
stations = pd.read_csv('Station Inventory EN.csv')
#grab the station ID from the wmo_id
station_id = stations['Station ID'][stations['WMO ID'] == 71296].iloc[0]

# create a big dataframe to hold the yearly weather data
wea_df = pd.DataFrame()
# Loop through the years requested
for year in tqdm(yearRanges, desc = 'looping through years:', position = 0):
    for month in tqdm(monthRanges, desc  = 'looping through months', position = 1):
        #now carry out the request
        data = Connector.get_weather_data(station_id, year, month)
        #try to fit the response parameters within a pandas dataframe
        try: 
            rawWeatherData = pd.read_csv(io.StringIO(data.content.decode('utf-8')))
            wea_df = wea_df.append(rawWeatherData)
        #spit out an error if you can't
        except:
            print('data received in an incorrect format for month:{}; year:{}... please review the raw request return'.format(month, year))

#reset the index now
wea_df = wea_df.reset_index(drop = True)

#put the data into a folder
Connector.data_printer(wea_df)

# %%
