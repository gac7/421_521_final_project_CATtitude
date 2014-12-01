#
#cat detection + log file of squirt instances 
#still missing email component to send weekly emails to user

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


def parsearguments():
    parser = argparse.ArgumentParser(description='object detection using cascade classifier')
    parser.add_argument('-i', '--image', help='image file name')
    parser.add_argument('-c', '--cascade', dest='cascadefilename', help='cascade file name',
                        default='models/cat/lbp/cascade.xml')
    parser.add_argument('-s', '--scalefactor', dest='scalefactor', type=float, default=1.1)
    parser.add_argument('-m', '--minneighbors', dest='minneighbors', type=int, default=3)
    parser.add_argument('-o', '--output', dest='output',
                        default='box/detect.jpg')
    return parser.parse_args()

def detect(imagefilename, cascadefilename, scalefactor, minneighbors):
    srcimg = cv.imread(imagefilename)
    if srcimg is None:
        print('cannot load image')
        sys.exit(-1)
    cascade = cv.CascadeClassifier(cascadefilename)
    objects = cascade.detectMultiScale(srcimg, scalefactor, minneighbors)
    count = len(objects)
    print('detection count: %s' % (count,))
    for (x, y, w, h) in objects:
        #print(x, y, w, h)
        cv.rectangle(srcimg, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return (srcimg, count)

def tumblrupload(count):
	tumblr_hostname = "CATsequencesCATalog.tumblr.com"
	addr_to = 'p3qcddbbzup89@tumblr.com'			
	addr_from = 'cattitude.catlog@gmail.com'
	user = 'cattitude.catlog'
	
	with open ("password.txt", "r") as myfile:
		password=myfile.readlines()
	
	msg = MIMEMultipart()
	msg['Subject'] = 'CATsequences delivered'
	msg['From'] = addr_from
	msg['To'] = addr_to
	file_to_upload = '../../imgdrop/img' + str(count) + '.png'
	#print file_to_upload
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


camera = picamera.PiCamera()
stream = picamera.array.PiRGBArray(camera)
camera.start_preview()
#	time.sleep(2)



connected = False
ser = serial.Serial("/dev/ttyACM0",9600)
time.sleep(5)
ser.write ('M106\n')
ser.write ('G4 S1\n')
ser.write('M107\n')
k = 1;

while True:
	#print('in the while loop')
	camera.resolution = (150,150)
	camera.capture('../../image_for_analysis/image.png', format='png')
	img = cv2.imread('../../image_for_analysis/image.png')
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imwrite('../../imgdrop/img' + str(k) + '.png', img)

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

		if count > 0:
			#print('cat detected!')

			ser.write ('M106\n')
			ser.write ('G4 P500\n')
			ser.write('M107\n')
	
        		while ser.read() == 1:
				ser.read()

			guilt_log = open("squirt.txt", "a")
			current_time = str(time.localtime())
			guilt_log.write("squirt instance at " + current_time +"\n")

			shutil.copy2('../../imgdrop/img' + str(k) + '.png','../../guiltCATalog')

			tumblrupload(k)
			
        
	os.remove('../../imgdrop/img' + str(k) + '.png')	
	k = k+1


