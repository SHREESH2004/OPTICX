import socket
import time
import pyttsx3
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading

HC05_MAC_ADDRESS = '00:23:00:01:5D:97'
PORT = 11
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def connect_bluetooth():
    # Initialize Bluetooth socket connection
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    sock.connect((HC05_MAC_ADDRESS, PORT))
    return sock

def start_reading(sock):
    try:
        print("Connected to HC-05 Bluetooth module. Waiting for distance data...")
        while True:
            data = sock.recv(1024).decode('utf-8').strip()
            if data:
                print(f"Received from HC-05: {data} cm")
                announcement = f"The distance is {data} centimeters."
                update_display(announcement)
                engine.say(announcement)
                engine.runAndWait()
            time.sleep(1)
    except Exception as e:
        print("Error reading from Bluetooth:", e)
        sock.close()

def stop_reading():
    messagebox.showinfo("Info", "Stopped reading from HC-05.")

def update_display(message):
    display_area.config(state=tk.NORMAL)  # Enable the text area for editing
    display_area.insert(tk.END, message + '\n')  # Append new message
    display_area.yview(tk.END)  # Scroll to the end
    display_area.config(state=tk.DISABLED)  # Disable editing

# Create the GUI window
root = tk.Tk()
root.title("Arduino Data Reader")

# Create a scrolled text area for displaying results
display_area = scrolledtext.ScrolledText(root, width=60, height=20, state=tk.DISABLED)
display_area.pack(pady=10)

# Start Bluetooth connection and begin reading
sock = connect_bluetooth()

start_button = tk.Button(root, text="Start Reading", command=lambda: threading.Thread(target=start_reading, args=(sock,), daemon=True).start())
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Reading", command=stop_reading)
stop_button.pack(pady=10)

# Run the GUI event loop
root.mainloop()
