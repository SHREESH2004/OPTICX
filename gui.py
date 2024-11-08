import serial
import time
import requests
import pyttsx3
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading

# Initialize serial communication
ser = serial.Serial('COM11', 9600, timeout=1)
time.sleep(5)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# Global variables for location tracking
prev_latitude, prev_longitude = None, None

def get_location():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        location = data['loc']
        latitude, longitude = location.split(',')
        city = data.get('city', 'Unknown city')
        region = data.get('region', 'Unknown region')
        country = data.get('country', 'Unknown country')
        return float(latitude), float(longitude), city, region, country
    except Exception as e:
        print(f"Error fetching location: {e}")
        return None, None, None, None, None

def get_weather(latitude, longitude):
    api_key = '7d8abffc740b2a9a0ce052cbbe98647f'  # Your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return weather_description, temperature
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None, None

def start_reading():
    global prev_latitude, prev_longitude
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Received from Arduino: {line} cm")
            latitude, longitude, city, region, country = get_location()

            if latitude and longitude:
                if latitude != prev_latitude or longitude != prev_longitude:
                    weather_description, temperature = get_weather(latitude, longitude)

                    announcement = (f"{line} centimeters, and your current location is in {city}, {region}, {country}, "
                                    f"approximately latitude {latitude} and longitude {longitude}.")

                    if weather_description and temperature:
                        announcement += (f" The current weather is {weather_description} "
                                         f"with a temperature of {temperature}°C.")

                    prev_latitude, prev_longitude = latitude, longitude
                else:
                    announcement = f"{line} centimeters, same location."

                    weather_description, temperature = get_weather(latitude, longitude)
                    if weather_description and temperature:
                        announcement += (f" The weather remains {weather_description} "
                                         f"with a temperature of {temperature}°C.")

                # Update the GUI with the announcement
                update_display(announcement)
                engine.say(announcement)
                engine.runAndWait()
            else:
                update_display("Could not retrieve location.")
            time.sleep(1)

def stop_reading():
    ser.close()
    messagebox.showinfo("Info", "Stopped reading from Arduino.")

def update_display(message):
    display_area.config(state=tk.NORMAL)  # Enable the text area for editing
    display_area.insert(tk.END, message + '\n')  # Append new message
    display_area.yview(tk.END)  # Scroll to the end
    display_area.config(state=tk.DISABLED)  # Disable editing

# Create the GUI window
root = tk.Tk()
root.title("Arduino Data Reader")

# Create buttons
start_button = tk.Button(root, text="Start Reading", command=lambda: threading.Thread(target=start_reading, daemon=True).start())
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Reading", command=stop_reading)
stop_button.pack(pady=10)

# Create a scrolled text area for displaying results
display_area = scrolledtext.ScrolledText(root, width=60, height=20, state=tk.DISABLED)
display_area.pack(pady=10)

# Run the GUI event loop
root.mainloop()
