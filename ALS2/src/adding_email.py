#
#Quasi-live facial recognition works as of 11/16/14
#

import io
import time
import picamera
import cv2
import numpy as np
import picamera.array
import serial
import os
import smtplib

#creating in memory stream



camera = picamera.PiCamera()
#stream = picamera.array.PiRGBArray(camera)
camera.start_preview()
#	time.sleep(2)

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30))#, flags = cv2.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

cascade = cv2.CascadeClassifier("../data/haarcascades/haarcascade_frontalface_alt.xml")
nested  = cv2.CascadeClassifier("../data/haarcascades/haarcascade_eye.xml")

connected = False
ser = serial.Serial("/dev/ttyACM0",9600)
time.sleep(5)
ser.write ('M106\n')
ser.write ('G4 S1\n')
ser.write('M107\n')




while True:
	camera.resolution = (120,120)
	camera.capture('image.png', format='png')

    	img = cv2.imread('image.png')
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
        rects = detect(gray, cascade)
        
        draw_rects(img, rects, (0, 255, 0))
        for x1, y1, x2, y2 in rects:
       		roi = gray[y1:y2, x1:x2]
       		vis_roi = img[y1:y2, x1:x2]
       		cv2.imshow('subregion', vis_roi)
         	subrects = detect(roi.copy(), nested)
            	draw_rects(vis_roi, subrects, (255, 0, 0))
	   	log = open("facefile.txt", "a")
	   	log.write("found a face")
	   	
	

		#ser.write("1")
		ser.write ('M106\n')
		ser.write ('G4 P500\n')
		ser.write('M107\n')

		guilt_log = open("squirt.txt", "a")
		current_time = str(time.localtime())
		guilt_log.write("squirt instance at " + current_time +"\n")	

        	while ser.read() == 1:
			ser.read()
	    
        