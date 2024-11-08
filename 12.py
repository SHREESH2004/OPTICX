import serial
import time
import requests
import pyttsx3

ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(5)

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)


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


prev_latitude, prev_longitude = None, None

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        print(f"Received from Arduino: {line} cm")
        time.sleep(1)

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

            print(announcement)
            engine.say(announcement)
            engine.runAndWait()
        else:
            print("Could not retrieve location.")
