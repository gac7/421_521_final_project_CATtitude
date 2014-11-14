import time
import picamera

with picamera.PiCamera() as camera:
	camera.start_preview()
	time.sleep(5)
	camera.capture('/home/pi/421_521_final_project_CATtitude/image.jpg')
	camera.stop_preview()
