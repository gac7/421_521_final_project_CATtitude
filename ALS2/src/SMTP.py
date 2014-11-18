import smtplib

def prompt(prompt) :
	return raw_input(prompt).strip()

fromaddr = prompt("From: ")
toaddrs = prompt("To: ").split()
print "Enter message, end with ^D (Unix) ir ^Z (Windows):"

# Add the From: and To: headers at the start!
msg = ("From 
