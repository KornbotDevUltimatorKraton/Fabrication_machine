import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200)

time.sleep(2)
ser.write("G0 X110\r\n")
time.sleep(1)
ser.close()
