#! usr/bin/python

import smtplib
import string, subprocess, time
import os


from email.mime.multipart import MIMEMultipart
from subprocess import call

smtpUser = 'cattitude.catlog@gmail.com'
smtpPass = 

toAdd = 'gcaldero@tulane.edu'
fromAdd = smtpUser

subject = 'CATsequences report'
header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject

cat_log = open('squirt.txt', 'r')
#cat_att = print cat_log.read()

body = cat_log.read()

print header + '\n' + body

#attachment = MIMEMultipart()
#attachment.attach('/home/pi/421_521_final_project_CATtitude/ALS2/src/squirt.txt')

s = smtplib.SMTP('smtp.gmail.com',587)

s.ehlo()
s.starttls()
s.ehlo()

s.login(smtpUser, smtpPass)
s.sendmail(fromAdd, toAdd, header + '\n\n' + body)

os.remove('/home/pi/421_521_final_project_CATtitude/ALS2/src/squirt.txt')
open('/home/pi/421_521_final_project_CATtitude/ALS2/src/squirt.txt', 'a')

s.quit()

