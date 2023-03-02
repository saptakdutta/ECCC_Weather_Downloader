#%% Libs
import pandas as pd
import io
import numpy as np
from tqdm import tqdm
from ConnLib import Connector
import argparse

#%%Parser commands
parser = argparse.ArgumentParser(description="""This code extracts hourly data from the ECCC historical weather database""")
parser.add_argument('-wmo_id', '--id', default= 71296,
                      help= 'This is the WMO_ID field on the ECCC site',
                      type= int)
parser.add_argument('-yearUpperRange', '--upperRange', default= 2024,
                      help= 'Upper year for download',
                      type= int)
parser.add_argument('-yearLowerRange','--lowerRange', default = 2022, 
                      help = 'Lower year for download', 
                      type = int)
parser.add_argument('-outputFormat','--outputFormat', default = 'parquet', 
                      help = 'specify the output format here', 
                      type = str)

#Parse arguments 
args = parser.parse_args()
wmo_id = args.id
upperYearRange = args.upperRange
lowerYearRange = args.lowerRange
dataFormat = args.outputFormat

#%% Program body
# wmo_id = 71296 #This is the WMO ID field in the ECCC site
# upperYearRange = 2023
# lowerYearRange = 2022

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
Connector.data_printer(wea_df, wmo_id, dataFormat)

# %%
