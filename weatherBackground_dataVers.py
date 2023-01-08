# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 00:19:22 2022

## Auto-Update Weather Background v.02

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
            'Weather_State_Previous',
            "Temp",
            'Date',
            'Time',
            'UserID',
            'Program_ProcessTime',
            'Program_ClockTime',
            'Change_Status',
            'Error_Status'      
            }

## Data Logging Dictionary Default Value
dataLogDefaultVal = "DEFAULT"

## Data Logging Dictionary
dataLogDict = dict.fromkeys(dataKeys, dataLogDefaultVal)



# =============================================================================
# ## File Names [Edit Here If Needed]
# =============================================================================
userFileName = 'userID.txt'
weatherFileName = 'weatherState.txt'
dataLogFileName = 'weatherData.csv'


# =============================================================================
# Main 
# =============================================================================
def main():
        
    ## Date and Time of Program Launch
    dateTimeLog()
    
    ## Read In or Generate User ID
    timeFunc(userID, userFileName)

    ## Get Previous Weather Status 
    myValue = weatherFileRead(weatherFileName)
    
    ## TODO
    ## Add Skip Feature if weather is unchanged
    
    ## Data Logging and  Collection
    myData = dataFileLoad(dataLogFileName)
    print("/n ***", myValue, "\n *** \n")
    
    

    
    ## API Key Printout
    print("This is a test")
    print(API_Key)
    
    ## Get Weather Status
    weather = timeFunc(weatherReport, API_Key)
    
    ## Convert Weather Status to Type (In Dictionary)
    key = weatherConversion(weather)
    
    
    ## Press Key Based on Weather Type
    keyPress(key)
    
    
    timeFunc(weatherReport, API_Key)
    
    print(dataLogDict)
    
    timeFunc(keyPress)
    
    
    ## Append and Write Data Log
    myData = myData.append(dataLogDict, ignore_index = True)
    myData.to_csv('weatherData.csv', index = False)

# =============================================================================
# Auxillary Functions
# =============================================================================





# =============================================================================
# ## Date and Time of Program Ran
# =============================================================================
def dateTimeLog():
    '''
    This function logs date and time, and updates dictionary with values
    '''
    dt = datetime.now()                                      ## Get Datetime
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
# ## File Handling for Weather State Tracking (Previous Value)
# =============================================================================
def weatherFileRead(weatherStateFileName):
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
    
 
    



    print("%s Process Time: " % functionName, processClockTotal)
    print("%s Clock Time: " % functionName, timeClockTotal)
    

    
    print("TIME FUNCTION VALUE TEST: ", myVal)
    
    return myVal
    




    
    
    
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
        
        ## TODO
        ## Create csv and skeleton here
        ## Break up Timestamp into min/hour/day/month/year
        ## Track weather state / time / change or not? / etc
        
        
        ## Dataframe Setup
        ## Weather State / Date / Time / Change Status / Error Status
        myData = pd.DataFrame({
            'Weather_State': pd.Series(dtype = 'str'),
            'Weather_State_Previous' : pd.Series(dtype = 'str'),
            'Temp' : pd.Series(dtype = 'str'),
            'Date' : pd.Series(dtype = 'str'),
            'Time' : pd.Series(dtype = 'str'),
            'UserID' : pd.Series(dtype = 'str'),
            'Program_ProcessTime' : pd.Series(dtype = 'float'),
            'Program_ClockTime' : pd.Series(dtype = 'float'),
            'Change_Status' : pd.Series(dtype = 'str'),
            'Error_Status' : pd.Series(dtype = 'str')
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
# ## OpenWeather Weather Data (JSON) Load
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




