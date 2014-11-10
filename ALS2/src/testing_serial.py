#! /usr/bin/python

import serial

connected = False

ser = serial.Serial('/dev/ttyACM0', 9600)

#time.sleep(2) 

while not connected:
	try:
	 serin = ser.read()
	except ValueError:
	 continue
	connected = True

ser.write("1")

while ser.read() == "1":
	ser.read()

ser.close() 
