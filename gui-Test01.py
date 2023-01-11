# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 22:30:59 2023


GUI Test 01
Assist from Chat GPT

@author: dforc
"""


import tkinter as tk
import requests
import os

# API key for OpenWeather

api_key = os.environ.get('Weather_API_Key')

def get_weather():
    zip_code = zip_entry.get()
    # send GET request to OpenWeather API
    url = f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&appid={api_key}'
    response = requests.get(url)
    # parse the JSON response
    data = response.json()
    # display the weather data in the GUI
    temp_label.config(text=f'Temperature: {data["main"]["temp"]}')
    weather_label.config(text=f'Weather: {data["weather"][0]["main"]}')
    loc_label.config(text = f'Location: {data["name"]}')
    

# create the GUI window
root = tk.Tk()
root.title('Weather App')

# create the zip code entry field
zip_label = tk.Label(root, text='Enter your zip code:')
zip_label.pack()
zip_entry = tk.Entry(root)
zip_entry.pack()

# create the 'Get Weather' button
get_weather_button = tk.Button(root, text='Get Weather', command=get_weather)
get_weather_button.pack()

# create the temperature and weather labels
temp_label = tk.Label(root, text='Temperature:')
temp_label.pack()
weather_label = tk.Label(root, text='Weather:')
weather_label.pack()
loc_label = tk.Label(root, text = "Location: ")
loc_label.pack()

root.mainloop()