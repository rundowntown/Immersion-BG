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

##
## 11/28 TODO: Set Hotkeys / Create Backgrounds / Set Continuous Run
## Set interval / Create Program Launch on Stream Deck


## Weather API Key from: https://openweathermap.org/
API_Key = os.environ.get('Weather_API_Key')


## Set Working Directory
os.chdir('C:\\Users\\dforc\\Desktop\\Immersion-BG')


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
    
    print("This is a test")
    print(API_Key)
    
    weather = weatherReport(API_Key)
    
    
    key = weatherConversion(weather)
    keyPress(key)




# =============================================================================
# Auxillary Functions
# =============================================================================

## Key Press Function
def keyPress(key):
    """
    This function takes in a key generated from weatherConversion()
    Triggers the hotkey to switch background State
    """
    pyautogui.keyDown("ctrl")
    pyautogui.press(key)
    pyautogui.keyUp("ctrl")



## OpenWeather Weather Data (JSON)
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
    


## Weather Determination
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




