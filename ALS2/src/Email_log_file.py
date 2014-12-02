#! usr/bin/python

#Creating and sending simple text messages with python 

import io
import time

import subprocess
import os
import sys
import smtplib
import email
from email.MIMEText import MIMEText


addr_to = 'gcaldero@tulane.edu'			

addr_from = 'cattitude.catlog@gmail.com'

user = 'cattitude.catlog'
	
with open ("password.txt", "r") as myfile:
	password=myfile.readlines()


file_to_upload = '/home/pi/421_521_final_project_CATtitude/ALS2/src/squirt.txt'
fp = open(file_to_upload, 'rb')
msg = MIMEText(fp.read())
			
msg['Subject'] = 'CATsequences report'
msg['From'] = addr_from
msg['To'] = addr_to

#print file_to_upload

msg['CATsequences report'] = 'The contents of %s' % file_to_upload
fp.close()

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(user, password)
server.sendmail(msg['From'], msg['To'], msg.as_string())

os.remove('/home/pi/421_521_final_project_CATtitude/ALS2/src/squirt.txt')
open('/home/pi/421_521_final_project_CATtitude/ALS2/src/squirt.txt', 'a')

server.quit()





