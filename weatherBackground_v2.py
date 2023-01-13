# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 00:19:22 2022

## Auto-Update Weather Background v2

## 1/13/23
## Last Edits before ChatGPT Co-pilot Assist

@author: dforc
"""

# =============================================================================
# Imports
# =============================================================================
## TODO If Required Que Install
import os
import requests
import json
import time
import re
import uuid
import schedule
import pyautogui
import pandas as pd
import tkinter as tk  ## GUI
from datetime import datetime

## Classes
import zipHandling

## Set AutoGUI Failsafe to 0 for Speed Increase on keyPress
pyautogui.PAUSE = 0

## Log Program Start Time
startProcessClock = time.process_time()   ## Process Time
startTimeClock = time.time()              ## Clock Time

## TODO
## 11/28 TODO: Set Hotkeys / Create Backgrounds / Set Continuous Run
## Set interval / Create Program Launch on Stream Deck

## TODO
## Notes 12/28
## Create Autoload API w Hidden Key For New Imports or Readme



## Weather API Key from: https://openweathermap.org/
API_Key = os.environ.get('Weather_API_Key')


## Set Working Directory From Absolute Path
absPath = os.path.abspath(__file__)          ## Absolute Path
dirPath = os.path.dirname(absPath)           ## Directory Path
os.chdir(dirPath)                            ## Set Directory

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
## Data Logging Dictionary Key Set
dataKeys = {'Date',
            'Time',
            'DateTime',
            'Weather_State', 
            'Weather_State_Previous',
            'Location',
            "Temp_F",                         ## Fahrenheit 
            "Humidity",
            'UserID',
            'Program_ProcessTime',
            'Program_ClockTime',
            'Change_Status'    
            }

## Data Logging Dictionary Default Value
dataLogDefaultVal = "EMPTY_DEFAULT"

## Data Logging Dictionary
dataLogDict = dict.fromkeys(dataKeys, dataLogDefaultVal)


# =============================================================================
# ## File Names [Edit Here If Needed]
# =============================================================================
userFileName = 'userID.txt'
weatherFileName = 'weatherState.txt'
zipFileName = 'zipCode.txt'
dataLogFileName = 'weatherData.csv'


# =============================================================================
# ## Main 
# =============================================================================
def main():
        
    ## Date and Time of Program Launch                         [Date/Time]
    dateTimeLog()
    
    ## Read In or Generate User ID and Zip                     [User ID]
    timeFunc(userID, userFileName)
    
    ## Get User Zip Code                                       [User ZIP]
    myZip = timeFunc(zipCode, zipFileName)
    
    ## Hold User API Variables in List to Pass to API        
    weatherVariables = [API_Key, myZip]
    
    ## Get Weather Status                                      [Weather Status]
    weather = timeFunc(weatherReport, weatherVariables)

    ## Get Previous Weather Status & Save New Weather          [Prev. W Status]
    previousWeather = timeFunc(weatherPreviousRead, weatherFileName)
    
    ## Update Saved Weather for Previous Tracking              [Prev. W Update]
    weatherPreviousWrite(weatherFileName, weather)
    
    ## Weather Change Handling                                 [Weather Key]
    weatherChange(weather, previousWeather)
    
    ## Total Run Time for Main                                 [Run Time End]
    mainTime(startProcessClock, startTimeClock)
 
    ## Data Logging and  Collection                            [Open Data Log]
    myData = dataFileLoad(dataLogFileName)
    
    ## Append and Write Data Log                               [Data Write]
    dataLogWrite(myData)
    

# =============================================================================
# 
# ---- Functions ----
#
# =============================================================================

# =============================================================================
# ## Date and Time of Program Ran
# =============================================================================
def dateTimeLog():
    '''
    This function logs date and time, and updates dictionary with values
    '''
    dt = datetime.now()                                      ## Get Datetime
    dataLogDict['DateTime'] = str(dt)                        ## Save DateTime
    dataLogDict['Date'] = dt.date()                          ## Save Date
    dataLogDict['Time'] = dt.time().replace(microsecond=0)   ## Save Time


# =============================================================================
# ## User ID Load/Create Function
# =============================================================================
def userID(userFileName):
    '''
    --> Reads in user ID
    %>% If user ID does not exist, creates ID and file (uuid)
    <-- Returns user ID
    '''
    
    ## Set FilePath
    filePath = dirPath + "\\" + userFileName
    
    ## Check if User ID Exists
    try:
        with open (filePath, encoding = 'utf8') as userID:
            myID = userID.read()
            
    ## Create UserID if File Does Not Exist  
    except FileNotFoundError:
        
        ## Generate Unique User ID (As String)
        myID = str(uuid.uuid4())
        ## Create File and Write User ID
        with open (filePath, 'a+', encoding = 'utf8', 
                   newline = '') as userID:
            userID.write(myID)
            
    ## Update Data Log Dictionary
    dataLogDict['UserID'] = myID
            
    return myID



# =============================================================================
# ## User ZIP Code
# =============================================================================
def zipCode(zipFileName):
    
    ## Set FilePath
    filePath = dirPath + "\\" + zipFileName
    
    ## Check if Zip Code Exists
    try:
        with open (filePath, encoding = 'utf8') as zipCode:
            myZip = zipCode.read()
            
    except FileNotFoundError:
        with open (filePath, 'a+', encoding = 'utf8',
                  newline = '') as zipCode:
            myZip = zipHandling.askZipCode()
            zipCode.write(myZip)
            
    return myZip


# =============================================================================
# ## Previous Weather State Tracking
# =============================================================================
def weatherPreviousRead(weatherStateFileName):
    '''
   --> Takes in Filename >> Checks for File
    %>% Creates Weather State File with 'default' if FileNotFound
    Note: [saves previous weather state]
    <-- Returns Previous Weather State
    '''
    
    ## Filepath from directory path + fileName
    filePath =  dirPath + "\\" + weatherStateFileName
    
    ## Check if File Already Exists: Read From File
    try:
        with open (filePath, encoding = 'utf8') as weatherSaved:
            myPreviousWeather = weatherSaved.read()
    
    ## If FIle does not exist, Create New File
    except FileNotFoundError:

        ## Open/Write fo File (a+ Read/Write/Create Setting)
        with open (filePath, 'a+', encoding = 'utf8',
                  newline = '') as weatherSaved:
            weatherSaved.write('default')
            
            myPreviousWeather = weatherSaved.read()
    
    ## Update Data Log Dictionary
    dataLogDict['Weather_State_Previous'] = myPreviousWeather
            
    return myPreviousWeather


# =============================================================================
# ## Update Saved Previous Weather to Current
# =============================================================================
def weatherPreviousWrite(weatherStateFileName, weatherState):
    'This function Saves (Writes) the Recently Updated Weather in a text file'
    
    ## Filepath from directory path + fileName
    filePath =  dirPath + "\\" + weatherStateFileName
    
    ## Over-Write Previous Weather
    with open (filePath, 'w+', encoding = 'utf8') as weatherSaved:
        weatherSaved.write(weatherState)


# =============================================================================
# ## Process/Timer of Function Logger
# =============================================================================
def timeFunc(function, value = ''):
    '''
    This function logs process and time duration for selected function
    --> Takes in a function and value(s)
    %>% Updates Data Dictionary with duration times
    <-- Returns value produced from input function
    '''
    
    ## Get Function Name
    functionName = function.__name__
    
    ## Start Time Log [Process and Clock]
    startProcessClock = time.process_time()   ## Process Time
    startTimeClock = time.time()              ## Clock Time
    
    ## Run Function to be Timed
    myVal = function(value)
    
    ## Total Run Time for Process and Time [Rounded 5 Digits]
    processClockTotal = round(time.process_time() - startProcessClock, 5)
    timeClockTotal = round(time.time() - startTimeClock, 5)
    
    ## Update Data Log Dictionary
    dataLogDict[functionName + '_ProcessTime'] = processClockTotal
    dataLogDict[functionName + '_ClockTime'] = timeClockTotal
    
    return myVal


# =============================================================================
# ## Main Program Timer
# =============================================================================
def mainTime(startProcessClock, startTimeClock ):
    'Tracks Entire Program Run Time'
    
    ## Total Run Time for Process and Time
    processClockTotal = round(time.process_time() - startProcessClock, 5)
    timeClockTotal = round(time.time() - startTimeClock, 5)
    
    ## Update Data Log Dictionary
    dataLogDict['Program_ProcessTime'] = processClockTotal
    dataLogDict['Program_ClockTime'] = timeClockTotal
    

# =============================================================================
# ## Weather Change Handling Function
# =============================================================================
def weatherChange(weather, previousWeather):
    '''
    This function converts weather to weatherKey and triggers hotkey
    %>% Calls weatherConversion() for Key
    %>% Presses Hotkey attached to Weather
    %>% Determines If Change In Weather Occured
    '''
    
    ## Convert Weather to Associated Hotkey Action
    myKey = timeFunc(weatherConversion, weather)
    
    ## Press Hotkey
    timeFunc(keyPress, myKey)
    
    ## Weather Change Status
    if weather != previousWeather:
        dataLogDict['Change_Status'] = "Yes"
    else:
        dataLogDict['Change_Status'] = "No"
        


# =============================================================================
# ## Data Collection Log 
# =============================================================================
def dataFileLoad(dataFile):
    '''
    This function checks for and reads in the data log .csv
    %>% If the file does not exist, it creates a data log skeleton
    <-- Returns pandas data log dataframe
    '''

    ## Open Data Log .csv File
    try:
        myData = pd.read_csv(dataFile)
    
    ## If file does not exist, create file
    except FileNotFoundError:

        ## Dataframe Setup
        ## Weather State / Date / Time / Change Status / Error Status
        myData = pd.DataFrame({
            'Date' : pd.Series(dtype = 'str'),
            'Time' : pd.Series(dtype = 'str'),
            'DateTime' : pd.Series(dtype = 'str'),
            'Weather_State': pd.Series(dtype = 'str'),
            'Weather_State_Previous' : pd.Series(dtype = 'str'),
            'Location' : pd.Series(dtype = 'str'),
            'Temp_F' : pd.Series(dtype = 'float'),
            'Humidity' : pd.Series(dtype = 'float'),
            'UserID' : pd.Series(dtype = 'str'),
            'Program_ProcessTime' : pd.Series(dtype = 'float'),
            'Program_ClockTime' : pd.Series(dtype = 'float'),
            'Change_Status' : pd.Series(dtype = 'str')
            })
        
        ## Set Index Name
        myData.index.name = "Update_ID"
        
        ## Save New Dataframe to CSV
        myData.to_csv(dataFile, encoding = 'utf8')
        
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
# ## Write Log Data to CSV Function    
# =============================================================================
def dataLogWrite(myData):
    """
    %>% Converts Data Log Dictionary to a dataframe
    %>% Concatenates (Adds) New Data to Existing Dataset
    %>% Writes File
    """
    
    ## Convert Log Dict to DataFrame
    dataLogData = pd.DataFrame([dataLogDict], 
                               columns = dataLogDict.keys())
    ## Add New Data to Previous Data
    myData = pd.concat([myData, dataLogData])

    ## Write to CSV
    myData.to_csv('weatherData.csv', index = False)
    


# =============================================================================
# ## OpenWeather Weather Data (JSON) Load
# =============================================================================
def weatherReport(weatherVariables):
    """
    This Function can tell you the weather
    --> Calls a openweather API and saves specific weather data
    --> Responds in channel with relevant weather data
    """
    
    ## Geocoding : https://openweathermap.org/api/geocoding-api
    
    ## Weather API Key from: https://openweathermap.org/
    weather_api = weatherVariables[0]
    zipCode = weatherVariables[1]
    zipCode = '05059'
    url_W = f'http://api.openweathermap.org/data/2.5/weather?zip={zipCode},us&appid={weather_api}&units=imperial'

            
    response = requests.get(url_W)
    weatherData = json.loads(response.text)
    
    ## Weather Data Info
    temp = weatherData['main']['temp']                     ## Current Temp [F]
    tempMin = weatherData['main']['temp_min']              ## Max Temp [F]
    tempMax = weatherData['main']['temp_max']              ## Min Temp [F]
    humidity = weatherData['main']['humidity']             ## Humidity
    weatherState = weatherData['weather'][0]['main']       ## Weather Condition 
    locName = weatherData['name']                          ## Location Name
    
    
    ## Update Data Log Dictonary
    dataLogDict['Weather_State'] = weatherState
    dataLogDict['Temp_F'] = temp                           ## Fahrenheit 
    dataLogDict['Humidity'] = humidity
    dataLogDict['Location'] = locName
    
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

    
# =============================================================================
# ## TODO 12/10/22
# - Check if conditions changed
# - Trigger without keypress (no interrupt)
# - autorun and .exe with stream deck icon/app
# - make background assets
# =============================================================================

main()




