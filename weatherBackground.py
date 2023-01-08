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
absPath = os.path.abspath(__file__)          ## Absolute Path
dirPath = os.path.dirname(absPath)           ## Directory Path
os.chdir(dirPath)                            ## Set Directory

print(absPath)
print(dirPath)

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
dataLogDict = {
    'Weather_State' : '2',
    'Date' : '4',
    'Time' : '5',
    'Change_Status' : '5',
    'Error_Status' : '6'
    }


# =============================================================================
# Main 
# =============================================================================
def main():
    
    dt = datetime.now()
    print("PROGRAM START: ", dt)
    
    
    ## Get Previous Weather Status 
    myValue = weatherFileRead('weatherState.txt')
    
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

    

# =============================================================================
# Auxillary Functions
# =============================================================================


    

# =============================================================================
# ## File Handling for Weather State Tracking (Previous Value)
# =============================================================================
def weatherFileRead(fileName):
    '''
   --> Takes in Filename >> Checks for File
    %>% Creates Weather State File with 'default' if FileNotFound
    Note: [saves previous weather state]
    <-- Returns Previous Weather State
    '''
    
    ## Filepath from directory path + fileName
    filePath =  dirPath + "\\" + fileName
    
    ## Check if File Already Exists: Read From File
    try:
        with open (filePath, encoding = 'utf8') as weatherSaved:
            myWeather = weatherSaved.read()
    
    ## If FIle does not exist, Create New File
    except FileNotFoundError:

        ## Open/Write fo File (a+ Read/Write/Create Setting)
        with open (filePath, 'a+', encoding = 'utf8',
                  newline = '') as weatherSaved:
            weatherSaved.write('default')
            
            myWeather = weatherSaved.read()
            
    return myWeather
    


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
            'Change_Status' : pd.Series(dtype = 'str'),
            'Error_Status' : pd.Series(dtype = 'str')
            })
        
        ## Set Index Name
        myData.index.name = "Update_ID"
        
        ## Save New Dataframe to CSV
        myData.to_csv('weatherData.csv', encoding = 'utf8')
        
        
    return myData


# =============================================================================
# ## Timestamp Date/Time Handling
# =============================================================================


# =============================================================================
# ## Data
# =============================================================================
        
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




