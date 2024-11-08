import serial
import time
import pyttsx3

ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(5)

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        print(f"Received from Arduino: {line} cm")
        time.sleep(0.001)

        engine.say(f"{line} centimeters")
        engine.runAndWait()
