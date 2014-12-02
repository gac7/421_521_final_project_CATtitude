#! usr/bin/python

#Creating and sending simple text messages with python 
#Note that Rasp Pi cron is set up to send weekly logs calling this .py code
#hat-tip: python docs 
#https://docs.python.org/2/library/email-examples.html

import io
import time

import subprocess
import os
import sys
import smtplib
import email
from email.MIMEText import MIMEText

#setting up email info
addr_to = 'gcaldero@tulane.edu'			

addr_from = 'cattitude.catlog@gmail.com'

user = 'cattitude.catlog'
#password information "gitignored" by separate .txt file 	
with open ("password.txt", "r") as myfile:
	password=myfile.readlines()

#calling the squirt log file that provides timestamped info of squirting instances based on cats detected in Cat_Detector_v3.py
file_to_upload = '/home/pi/421_521_final_project_CATtitude/ALS2/src/squirt.txt'
fp = open(file_to_upload, 'rb') #creating blank text/message
msg = MIMEText(fp.read())
			
msg['Subject'] = 'CATsequences report'
msg['From'] = addr_from
msg['To'] = addr_to

#message body contains the contents of the squirt text file
msg['CATsequences report'] = 'The contents of %s' % file_to_upload
fp.close()

#server information through smtp to actually send email
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(user, password)
server.sendmail(msg['From'], msg['To'], msg.as_string())

#removing contents of log so that each weekly email contains just that week's worth of information
os.remove('/home/pi/421_521_final_project_CATtitude/ALS2/src/squirt.txt')
open('/home/pi/421_521_final_project_CATtitude/ALS2/src/squirt.txt', 'a')

server.quit()





