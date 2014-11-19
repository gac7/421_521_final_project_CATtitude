import smtplib
import string, subprocess, time


from email.mime.multipart import MIMEMultipart
from subprocess import call

smtpUser = 'gacaldero@gmail.com'
smtpPass = '11Caniacs'

toAdd = 'gcaldero@tulane.edu'
fromAdd = smtpUser

subject = 'so cant figure out as an attachment but can put things in body...ugly but works!!'
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

s.quit()
