import smtplib

def prompt(prompt):
	return raw_input(prompt).strip()

fromaddr = prompt("From: ")
toaddrs = prompt("To: ").split()
print "Enter messsage, end with ^D (Unix) or ^Z (Windows)"

#add the from: and to: headers at the start!
msg = ("From: %s\r\nTo: %s\r\n\r\n"
	% (fromaddr, ", "/join(toaddrs)))

while 1:
	try:
		line - raw_input()
	except EOFError:
		break
	if not line:
		break
	msg = msg + line

print "Message length is" + repr(len(msg))

server= smtplib.SMTP('localhost')
server.setdebuglevel(1)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
