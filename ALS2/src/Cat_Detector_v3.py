############################################
#CATtitude
#Working version as of 12/2/2014
#Ian Kinstlinger and Gisele Calderon
#BioE521 Microcontroller Applications
############################################

#Note that for this file to work, it must be executed from /ALS2/src 
#! usr/bin/python

import io
import time
import picamera
import cv2
import numpy as np
import picamera.array
import serial
import subprocess
from subprocess import Popen
import argparse
import os
import re
import sys
import cv2 as cv
import shutil
import smtplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEBase import MIMEBase
from email import Encoders

###########
#First we define methods called later within the code
###########

#This section defines variables for pattern recognition to detect cats
#this code was adapted from github repo cat-fancier by user wellflat
#https://github.com/wellflat/cat-fancier
def parsearguments():
    parser = argparse.ArgumentParser(description='object detection using cascade classifier')
    parser.add_argument('-i', '--image', help='image file name') 
	#note that these add_argument lines are setting up the variables used in the detect method defined below
    parser.add_argument('-c', '--cascade', dest='cascadefilename', help='cascade file name',
                        default='models/cat/lbp/cascade.xml') 
						#this references cascade files in the same repo
    parser.add_argument('-s', '--scalefactor', dest='scalefactor', type=float, default=1.1)
    parser.add_argument('-m', '--minneighbors', dest='minneighbors', type=int, default=3)
    parser.add_argument('-o', '--output', dest='output',
                        default='box/detect.jpg')
    return parser.parse_args()

	
#This section defines criteria for cat detection
#adapted from the same repo by wellflat - thanks!
def detect(imagefilename, cascadefilename, scalefactor, minneighbors): #taking in the args from parseargs()
    srcimg = cv.imread(imagefilename) 
    if srcimg is None:
        print('cannot load image')
        sys.exit(-1)
    cascade = cv.CascadeClassifier(cascadefilename) #this uses the built-in functionality of the OpenCV package
    objects = cascade.detectMultiScale(srcimg, scalefactor, minneighbors) #same logic as used with the Haar cascades approach
    count = len(objects) #this is the number of cats detected
	# we treat this as a binary value - in determining the system response, count is either zero or non-zero (multiple cats has no influence)
    print('detection count: %s' % (count,)) #comment this line if you don't want the console to indicate when each detection is happening
    for (x, y, w, h) in objects:
        #print(x, y, w, h)
        cv.rectangle(srcimg, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return (srcimg, count)

	
#This section sets up tumblr upload via email
#this code was adapted from a Raspicam photobooth project by Chris Evans (github user drumminhands)
# git repo: https://github.com/drumminhands/drumminhands_photobooth
def tumblrupload(filecount): #filecount is an input so the upload is directed to the correct image file
	tumblr_hostname = "CATsequencesCATalog.tumblr.com"
	addr_to = 'p3qcddbbzup89@tumblr.com' #secret email provided by tumblr
	addr_from = 'cattitude.catlog@gmail.com'
	user = 'cattitude.catlog'
	
	with open ("password.txt", "r") as myfile:
		password=myfile.readlines() #workaround to avoid storing password in plaintext
	
	msg = MIMEMultipart()
	msg['Subject'] = 'CATsequences delivered' #The email subject line becomes the Tumblr caption
	msg['From'] = addr_from
	msg['To'] = addr_to
	file_to_upload = '../../imgdrop/img' + str(filecount) + '.png' 
	#print file_to_upload #uncomment to verify the filename
	fp = open(file_to_upload, 'rb')
	part = MIMEBase('image', 'gif')
	part.set_payload( fp.read() )
	Encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file_to_upload))
	fp.close()
	msg.attach(part)
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(user, password)
	server.sendmail(msg['From'], msg['To'], msg.as_string())
	server.quit()
	
	
#########
#This section is a security feature to provide alerts if excessive squirting occurs
#########	
def alertemail():
	addr_to = 'ian.kinstlinger@gmail.com' 
	addr_from = 'cattitude.catlog@gmail.com'
	user = 'cattitude.catlog'
	
	with open ("password.txt", "r") as myfile:
		password=myfile.readlines() #workaround to avoid storing password in plaintext
	
	msg = MIMEMultipart()
	msg['Subject'] = 'Alert! High frequency squirting activity ' 
	msg['From'] = addr_from
	msg['To'] = addr_to
	file_to_upload = 'alertemail.txt' 
	#print file_to_upload #uncomment to verify the filename
	fp = open(file_to_upload, 'rb')
	part = MIMEBase('image', 'gif')
	part.set_payload( fp.read() )
	Encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file_to_upload))
	fp.close()
	msg.attach(part)
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(user, password)
	server.sendmail(msg['From'], msg['To'], msg.as_string())
	server.quit()

##########
#Done defining things, now on to initializing the device
##########	

#This initializes the camera using the Python PiCamera library
#Note that the camera input will briefly occupy the entire monitor before disappearing and reappearing as a smaller window
camera = picamera.PiCamera()
stream = picamera.array.PiRGBArray(camera)
camera.start_preview()

######################
#Initialize the serial connection so that the Pi is communicating with the Arduino
#Arduino has RAMPS shield attached and is running Marlin firmware
#Credit for Marlin: Erik van der Zalm
#Git repo for Marlin: https://github.com/ErikZalm/Marlin
#When running Marlin, the Arduino will wait to recieve standard gcode commands

ser = serial.Serial("/dev/ttyACM0",9600) 
#One possible failure mode is if the Arduino is assigned a different Serial port id (i.e. ttyACM1). If this happens, change port id here
time.sleep(5) 
#Arduino needs a few seconds to initialize before receiving any gcode

#ser.write ('M106\n') #comment these 3 ser.write lines back in if you want the solenoid valve to actuate on startup (useful for testing)
#ser.write ('G4 S1\n')
#ser.write('M107\n')
########################

##############
#Here is the main loop in the code!
#After the serial connection is initialized, this loop is run continuously
#Each run through the while loop is taking and processing of a discete image. This is how we approximate real-time face recognition
##############

k = 1 #This variable increments on each pass thru the loop to change the filename 
consecutive = 0 #This variable tracks consecutive squirts as part of a safety feature
# Incrementing value was a convenient way to consistent reference files as they were stored and accessed by multiple lines of code


while True:
	#print('in the while loop')
	
	camera.resolution = (150,150) 
	#Resolution is the primary determinant of the frequency of photo capture. 
	#Lower resolution leads to faster image processing and faster runs through the loop
	#150x150 px seems to work well for pseudo-real time analysis with reliable detection
	
	camera.capture('../../image_for_analysis/image.png', format='png')
	img = cv2.imread('../../image_for_analysis/image.png') #Image replaced each time through the loop
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Actual pattern recognition is done in greyscale
	#This actually helps recognize a greater variety of cats
	cv2.imwrite('../../imgdrop/img' + str(k) + '.png', img) #Image retained with incrementing number

	##The next 10 lines of code once again from Cat-fancier
	
	args = parsearguments()
	#print('cascade file: %s' % (args.cascadefilename,))
	imagedir = '../../image_for_analysis'
	pattern = re.compile('.*[.](jpg|jpeg|png|bmp|gif)$')
	images = [image for image in os.listdir(imagedir) if re.match(pattern, image)]
	#print('target files: %s' % (len(images), ))
	for i, image in enumerate(images):
    		imagesrc = os.path.join(imagedir, images[i])
    		result, count = detect(imagesrc, args.cascadefilename,
                    args.scalefactor, args.minneighbors)
		
		#######
		#Everything below here is what happens when a cat is detected
		#######
		
		if count > 0: #1 or more cats found
			#print('cat detected!') #Good for testing

			##Response 1) SPRAY THE MISBEHAVING CAT
			ser.write ('M106\n') #Send 12V to MOSFET pin D9
			ser.write ('G4 P500\n') #Pause. The P value is the duration that the valve will be open (in ms)
			ser.write('M107\n') #Cut off the voltage, closing the valve
	
        		while ser.read() == 1: #this was suggested online to make sure the Arduino keeps reading. 
					ser.read()
			
			##Response 2) Record the cat squirt in a log file
			guilt_log = open("squirt.txt", "a") #This is the local log file
			current_time = str(time.localtime())
			guilt_log.write("squirt instance at " + current_time +"\n") #Time stamp the squirt incident in the log
			#Cron is set up to email this file weekly

			#If a cat was indeed found, we want to keep the image in the Guilt CATalog
			shutil.copy2('../../imgdrop/img' + str(k) + '.png','../../guiltCATalog')
			
			##Response 3) Immortalize the misbehaving cat's mugshot on the CATsequencesCATalog 
			tumblrupload(k)
			
			##Increase the number of consecutive squirts
			consecutive = consecutive + 1
			
			if consecutive > 4: #Too many consecutive squirts, possible malfunction (safety feature)
				alertemail() #Send an alert email
				time.sleep(300) #Take a 5 minute break
				#Note that consecutive is not reset here, so if there is a malfunction, CATtitude will keep stopping for 5 minutes every time it squirts (safety feature)
			
        else
			consecutive = 0
			
	os.remove('../../imgdrop/img' + str(k) + '.png') #All done with this file. If there was a cat, it's in the guilt CATalog. If not, OK to delete
	
	k = k+1


