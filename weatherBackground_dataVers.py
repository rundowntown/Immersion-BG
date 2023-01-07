# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 00:19:22 2022

## Auto-Update Weather Background v.02

@author: dforc
"""

# =============================================================================
# Imports
# =============================================================================
import os
import requests
import json
import time
import uuid
import schedule
import pyautogui
import pandas as pd
from datetime import datetime

## TODO
## 11/28 TODO: Set Hotkeys / Create Backgrounds / Set Continuous Run
## Set interval / Create Program Launch on Stream Deck


## TODO
## Notes 12/28
## Create Autoload API w Hidden Key For New Imports or Readme
## Add Data Collection CSV

## TODO
## 1/1/23
## Add Logging Errors for All Errors in Data Log

## Weather API Key from: https://openweathermap.org/
API_Key = os.environ.get('Weather_API_Key')


## Set Working Directory From Absolute Path
abspath = os.path.abspath(__file__)        ## Absolute Path
dname = os.path.dirname(abspath)           ## Directory Path
os.chdir(dname)                            ## Set Directory


weather = ""

# =============================================================================
# ## Hotkeys 
# Edit Value for Key to change Hotkey
# =============================================================================
hotkeyDict = {
    "default" : "0",
    "clear" : "1",
    "cloud" : 'a',
    "drizzle" : "3",
    "thunder" : "4",
    "rain" : "5",
    "snow" : "6"
    }


# =============================================================================
# ## Data Logging Dictionary
# =============================================================================

# default_val = 'DEFAULT'
# dataLogDict = {
#     'Weather_State' : default_val,
#     'Date' : default_val,
#     'Time' : default_val,
#     'Program_ProcessTime' : 'DEFAULT',
#     'Program_ClockTime '
#     'Change_Status' : 'DEFAULT',
#     'Error_Status' : 'DEFAULT'
#     }




#             'Weather_State': pd.Series(dtype = 'str'),
#             'Date' : pd.Series(dtype = 'str'),
#             'Time' : pd.Series(dtype = 'str'),
#             'Program_ProcessTime' : pd.Series(dtype = 'str'),
#             'Program_ClockTime' : pd.Series(dtype = 'str'),
#             'weatherReport_ProcessTime' : pd.Series(dtype = 'str'),
#             'weatherReport_ClockTime' : pd.Series(dtype = 'str'),
#             'hotKeyPress_ProcessTime' : pd.Series(dtype = 'str'),
#             'hotKeyPress_ClockTime' : pd.Series(dtype = 'str'),
#             'Change_Status' : pd.Series(dtype = 'str'),
#             'Error_Status' : pd.Series(dtype = 'str')

## Data Logging Dictionary Key Set
dataKeys = {'Weather_State', 
            'Date',
            'Time',
            'Program_ProcessTime',
            'Program_ClockTime',
            'weatherReport_ProcessTime',
            'weatherReport_ClockTime',
            'hotKeyPress_ProcessTime',
            'hotKeyPress_ClockTime',
            'Change_Status',
            'Error_Status'      
            }

## Data Logging Dictionary Default Value
dataLogDefaultVal = "DEFAULT"

## Data Logging Dictionary
dataLogDict = dict.fromkeys(dataKeys, dataLogDefaultVal)




# =============================================================================
# Main 
# =============================================================================
def main():
        
    ## Program Date and Time Run
    dateTimeLog()
    
    ##ID
    userID()

    ## Get Previous Weather Status 
    myValue = weatherFileRead()
    
    ## TODO
    ## Add Skip Feature if weather is unchanged
    
    ## Data Logging and  Collection
    myData = dataFileLoad()
    print("/n ***", myValue, "\n *** \n")
    
    
    ## Append and Write Data Log
    myData = myData.append(dataLogDict, ignore_index = True)
    myData.to_csv('weatherData.csv', index = False)
    
    ## API Key Printout
    print("This is a test")
    print(API_Key)
    
    ## Get Weather Status
    weather = weatherReport(API_Key)
    
    ## Convert Weather Status to Type (In Dictionary)
    key = weatherConversion(weather)
    
    
    ## Press Key Based on Weather Type
    keyPress(key)
    
    
    timeFunc(weatherReport, API_Key)
    

# =============================================================================
# Auxillary Functions
# =============================================================================



# =============================================================================
# ## User ID Function
# =============================================================================
def userID():
    '''
    --> Reads in user ID
    %>% If user ID does not exist, creates ID and file
    <-- Returns user ID
    '''
         
    ## Check if User ID Exists
    try:
        with open ('..\\Immersion-BG\\userID.txt',
                   encoding = 'utf8') as userID:
            myID = userID.read()
            
    ## Create UserID if File Does Not Exist  
    except FileNotFoundError:
        
        ## Generate Unique User ID (As String)
        myID = str(uuid.uuid4())
        
        with open ('..\\Immersion-BG\\userID.txt', 'a+', encoding = 'utf8',
                   newline = '') as userID:
            userID.write(myID)
            
    return myID
            
    
# =============================================================================
# ## File Handling for Weather State Tracking (Previous Value)
# =============================================================================
def weatherFileRead():
    '''
    --> Checks for previous Weather State
    %>% Creates weatherState.txt with 'default' if FileNotFound
    <-- Returns Previous Weather State
    '''

    ## Check if File Already Exists: Read From File
    try:
        with open ('..\\Immersion-BG\\weatherState.txt', 
                   encoding = 'utf8') as weatherSaved:
            myWeather = weatherSaved.read()
    
    ## If FIle does not exist, Create New File
    except FileNotFoundError:

        ## Open/Write fo File (a+ Read/Write/Create Setting)
        with open ('..\\Immersion-BG\\weatherState.txt', 'a+', encoding = 'utf8',
                  newline = '') as weatherSaved:
            weatherSaved.write('default')
            myWeather = weatherSaved.read()
            
    return myWeather
    


# =============================================================================
# ## Time Function
# =============================================================================
## TODO 1/7/23
## Save Time Values In Correct Dict Location
 
def timeFunc(function, value):
    
    ## Get Function Name
    functionName = function.__name__
    
    ## Start Time
    startProcessClock = time.process_time()   ## Process Time
    startTimeClock = time.time()              ## Clock Time
    
    ## Function Run
    myVal= function(value)
    
    ## End Time
    processClockTotal = time.process_time() - startProcessClock
    timeClockTotal = time.time() - startTimeClock
    
    print("%s Process Time: " % functionName, processClockTotal)
    print("%s Clock Time: " % functionName, timeClockTotal)

    
    print("TIME FUNCTION VALUE TEST: ", myVal)
    



# =============================================================================
# ## Date and Time Log
# =============================================================================
def dateTimeLog():
    
    dt = datetime.now()
    dataLogDict['Date'] = dt.date()
    dataLogDict['Time'] = dt.time().replace(microsecond=0)
    
    
    
    
# =============================================================================
# ## Data Collection Log 
# =============================================================================
def dataFileLoad():
    '''
    This function checks for and reads in the data log .csv
    %>% If the file does not exist, it creates a data log skeleton
    <-- Returns pandas data log dataframe
    '''
    
    ## Data File Name
    dataFileName = "weatherData.csv"
    
    ## Open Data Log .csv File
    try:
        myData = pd.read_csv(dataFileName)
    
    ## If file does not exist, create file
    except FileNotFoundError:
        
        ## TODO
        ## Create csv and skeleton here
        ## Break up Timestamp into min/hour/day/month/year
        ## Track weather state / time / change or not? / etc
        
        
        ## Dataframe Setup
        ## Weather State / Date / Time / Change Status / Error Status
        myData = pd.DataFrame({
            'Weather_State': pd.Series(dtype = 'str'),
            'Date' : pd.Series(dtype = 'str'),
            'Time' : pd.Series(dtype = 'str'),
            'Program_ProcessTime' : pd.Series(dtype = 'str'),
            'Program_ClockTime' : pd.Series(dtype = 'str'),
            'weatherReport_ProcessTime' : pd.Series(dtype = 'str'),
            'weatherReport_ClockTime' : pd.Series(dtype = 'str'),
            'hotKeyPress_ProcessTime' : pd.Series(dtype = 'str'),
            'hotKeyPress_ClockTime' : pd.Series(dtype = 'str'),
            'Change_Status' : pd.Series(dtype = 'str'),
            'Error_Status' : pd.Series(dtype = 'str')
            })
        
        ## Set Index Name
        myData.index.name = "Update_ID"
        
        ## Save New Dataframe to CSV
        myData.to_csv('weatherData.csv', encoding = 'utf8')
        
        
    return myData



# =============================================================================
# ## Key Press Function
# =============================================================================
def keyPress(key):
    """
    This function takes in a key generated from weatherConversion()
    Triggers the hotkey to switch background State
    """
    pyautogui.keyDown("ctrl")     ## Hold Key Down
    pyautogui.press(key)          ## Single Key Press
    pyautogui.keyUp("ctrl")       ## Release Held Down Key



# =============================================================================
# ## OpenWeather Weather Data (JSON)
# =============================================================================
def weatherReport(API_Key):
    """
    This Function can tell you the weather
    --> Calls a openweather API and saves specific weather data
    --> Responds in channel with relevant weather data
    """
    
    ## Geocoding : https://openweathermap.org/api/geocoding-api
    
    ## Weather API Key from: https://openweathermap.org/
    weather_api = API_Key
    
    lat = '44.4759'
    lon = '-73.2121'
    url_W = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s&units=imperial" \
           % (lat, lon, weather_api)
            
    response = requests.get(url_W)
    weatherData = json.loads(response.text)
    
    ## Weather Data Info
    temp = weatherData['main']['temp']                     ## Current Temp
    tempMin = weatherData['main']['temp_min']              ## Max Temp
    tempMax = weatherData['main']['temp_max']              ## Min Temp
    humidity = weatherData['main']['humidity']             ## Humidity
    weatherState = weatherData['weather'][0]['main']       ## Weather Condition 
    locName = weatherData['name']                          ## Location Name
    
    print(weatherData)
    
    print(weatherState)
    
    return(weatherState)
    

# =============================================================================
# ## Weather Determination Function
# =============================================================================
def weatherConversion(weather):
    """
    --> Determines Type of Weather from weatherReport()
    %% Selects Correct Key from Dictionary
    <-- Returns Key
    """
    myWeather = weather.lower()
    
    ## Documentation: https://openweathermap.org/weather-conditions
    
    if 'clear' in myWeather:                        ## Clear
        weatherKey = hotkeyDict["clear"]
    
    if 'cloud' in myWeather:                        ## Cloudy
        weatherKey = hotkeyDict["cloud"]   
        
    if 'drizzle' in myWeather:                      ## Drizzle
        weatherKey = hotkeyDict["drizzle"]
        
    if 'thunderstorm' in myWeather:                 ## Thunderstorm
        weatherKey = hotkeyDict["thunder"]
        
    if 'rain' in myWeather:                         ## Rain
        weatherKey = hotkeyDict["rain"]
    
    if 'snow' in myWeather:                         ## Snow
        weatherKey = hotkeyDict["snow"]
    
    else:                                           ## Default
        weatherKey = hotkeyDict["default"]
        
    return(weatherKey)


#def lastWeather(value):
    
    
# =============================================================================
# ## TODO 12/10/22
# - Check if conditions changed
# - Trigger without keypress (no interrupt)
# - autorun and .exe with stream deck icon/app
# - make background assets
# =============================================================================
    


# =============================================================================
# Program
# =============================================================================
schedule.every(1).seconds.do(main) 


main()




