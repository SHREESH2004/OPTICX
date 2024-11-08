import serial
import time

try:

    bluetooth = serial.Serial('COM11', 9600)
    time.sleep(2)

    print("Connected to HC-05 Bluetooth module on COM11. Waiting for data...")

    while True:
        if bluetooth.in_waiting > 0:
            distance_data = bluetooth.readline().decode().strip()
            print("Distance:", distance_data)
        time.sleep(0.5)

except serial.SerialException as e:
    print("Serial error:", e)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    bluetooth.close()
