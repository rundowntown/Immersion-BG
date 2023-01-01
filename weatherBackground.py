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

## TODO
## 11/28 TODO: Set Hotkeys / Create Backgrounds / Set Continuous Run
## Set interval / Create Program Launch on Stream Deck


## TODO
## Notes 12/28
## Create Autoload API w Hidden Key For New Imports or Readme
## Add Data Collection CSV

## Weather API Key from: https://openweathermap.org/
API_Key = os.environ.get('Weather_API_Key')


## Set Working Directory From Absolute Path
abspath = os.path.abspath(__file__)        ## Absolute Path
dname = os.path.dirname(abspath)           ## Directory Path
os.chdir(dname)                            ## Set Directory


weather = ""

# =============================================================================
# Hotkeys
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
# Main 
# =============================================================================
def main():
    
    ## Get Previous Weather Status 
    myValue = weatherFileRead()
    
    ## TODO
    ## Add Skip Feature if weather is unchanged
    
    ## Data Logging and  Collection
    dataCollect()
    print("/n ***", myValue, "\n *** \n")
    
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
def weatherFileRead():
    '''
   --> Checks for weatherState.txt
    %>% Creates weatherState.txt with 'default' if FileNotFound
    Note: [weatherState.txt saves previous weather state]
    <-- Returns Previous Weather State
    '''

    ## Check if File Already Exists: Read From File
    try:
        with open ('..\Immersion-BG\weatherState.txt', 
                   encoding = 'utf8') as weatherSaved:
            myWeather = weatherSaved.read()
    
    ## If FIle does not exist, Create New File
    except FileNotFoundError:

        ## Open/Write fo File (a+ Read/Write/Create Setting)
        with open('..\Immersion-BG\weatherState.txt', 'a+', encoding = 'utf8',
                  newline = '') as weatherSaved:
            weatherSaved.write('default')
            myWeather = weatherSaved.read()
            
    return myWeather
    


# =============================================================================
# ## Data Collection Log 
# =============================================================================
def dataCollect():
    
    dataFileName = "weatherData.csv"
    
    try:
        myData = pd.read_csv(dataFileName)
        
    except FileNotFoundError:
        
        ## TODO
        ## Create csv and skeleton here
        ## Break up Timestamp into min/hour/day/month/year
        ## Track weather state / time / change or not? / etc
        
        
        ## Date / Time / Weather State / Change Status / 
        myData = pd.DataFrame({
            'Weather State': pd.Series(dtype = 'int'),
            'Date' : pd.Series(dtype = 'int'),
            'Time' : pd.Series(dtype = 'int'),
            'Change_Status' : pd.Series(dtype = 'int')
            })
        
        
        
        print('wowEEEE')
        
        
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




