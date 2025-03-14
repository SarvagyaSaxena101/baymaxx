import serial
import time

# Set up serial communication (TX = GPIO14, RX = GPIO15)
ser = serial.Serial("/dev/serial0", 115200, timeout=1)

while True:
    number = 123  # Number to send
    ser.write(f"{number}\n".encode())  # Send number as a string
    print(f"Sent: {number}")
    time.sleep(1)
