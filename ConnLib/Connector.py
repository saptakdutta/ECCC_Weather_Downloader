import pandas as pd
import requests as req

# Define functions
def get_weather_data(station_id: int, year: int, month: int, day = '31', format = 'csv'):
    '''
    This function reads in a station ID, year and month in int32 format, converts it to str format, and carries out 
    a request for hourly climate data with ECCC's historic weather database. Note that the return is in plain text
    format, as their API does not support JSON returns. You will need to decode the response in 'utf-8' format
    using a method of your choosing in order to view the data in tabular format.
    '''

    url = 'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format='+format+'&stationID='+str(station_id)+'&Year='+str(year)+'&Month='+str(month)+'&Day='+str(day)+'&time=UTC&timeframe=1&submit=Download+Data'
    ret = req.get(url)
    if ret.status_code == 200:
        return ret
    else:
        print('Something went wrong with the API call, returning raw request return parametrs now:')
        return ret

def data_printer(df: pd.DataFrame, dataFormat: str = 'parquet'):
    '''
    By default this function saves weather data to parquet format; i.e., .parquet. If you insist on using CSVs
    you can specify this in the function call like so: data_printer(df, 'csv'). CSVs are slow and delete the 
    metadata you worked so hard to build. For large data dumps, they will be slow, inefficient and annoying
    to process afterwards. 
    '''
    maxdate = str(max(pd.to_datetime(df['Date/Time (UTC)']).dt.date))
    mindate = str(min(pd.to_datetime(df['Date/Time (UTC)']).dt.date))
    if (dataFormat == 'csv'):
        df.to_csv('Weather_Files\climate_data_{}_{}.csv'.format(mindate, maxdate), index=False)
    else:
        df.to_parquet('Weather_Files\climate_data_{}_{}.parquet'.format(mindate, maxdate), index = False)
    return 'Data has been saved to the \Weather_Files folder'

def error_logger():
    
    return 0