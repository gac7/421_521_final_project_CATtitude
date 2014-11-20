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

tumblr_hostname = "CATsequencesCATalog.tumblr.com"
	
addr_to = 'p3qcddbbzup89@tumblr.com'			

addr_from = 'cattitude.catlog@gmail.com'

user = 'cattitude.catlog'
	
password = 'chipotle'

msg = MIMEMultipart()
			
msg['Subject'] = 'Tumblr upload'
msg['From'] = addr_from
msg['To'] = addr_to
file_to_upload = '/home/pi/421_521_final_project_CATtitude/guiltCATalog/img1.png'
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







