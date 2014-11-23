#
#Quasi-live facial recognition works as of 11/16/14
#

import io
import time
import picamera
import cv2
import numpy as np
import picamera.array
import serial

#creating in memory stream


#with picamera.PiCamera() as camera:
#	camera.start_preview()
#	camera.capture_continous(stream, format= 'jpeg')
#	stream.truncate()
#	stream.seek(0)

camera = picamera.PiCamera()
#stream = picamera.array.PiRGBArray(camera)
camera.start_preview()
#	time.sleep(2)

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30))#, flags = cv2.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

cascade = cv2.CascadeClassifier("../data/haarcascades/haarcascade_frontalface_alt.xml")
nested  = cv2.CascadeClassifier("../data/haarcascades/haarcascade_eye.xml")

connected = False
ser = serial.Serial("/dev/ttyACM1",9600)
time.sleep(5)
ser.write ('M106\n')
ser.write ('G4 S1\n')
ser.write('M107\n')

while True:
	camera.resolution = (120,120)
	camera.capture('image.png', format='png')
#time.sleep(2)

#Construct a numpy array from the stream
#	data = np.fromstring(stream.getvalue(), dtype=np.uint8)

# "decode" the image from teh array, preserving color
    	img = cv2.imread('image.png')
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#cv2.imwrite('test2.png', img)
    	#width= cap.get(3)
    	#height = cap.get(4)
    	#print width
    	#fourcc = cv2.VideoWriter_fourcc(cv2.FFMPEG)
    	#print cv2.FFMPEG
    	# http://docs.opencv.org/trunk/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
    # http://note.sonots.com/SciSoftware/haartraining.html
    #http://docs.opencv.org/trunk/modules/contrib/doc/facerec/facerec_tutorial.html
    #fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    #out = cv2.VideoWriter('output.mjpg',fourcc, 20.0, (640,480))
    #out = cv2.VideoWriter('out.avi',cv2.FFMPEG('M','J','P','G'), 20, (int(width),int(height)))
    	#captured_frame_number = 0
    
   	
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #gray = cv2.equalizeHist(gray)

        	
        rects = detect(gray, cascade)
        
        draw_rects(img, rects, (0, 255, 0))
        for x1, y1, x2, y2 in rects:
       		roi = gray[y1:y2, x1:x2]
       		vis_roi = img[y1:y2, x1:x2]
       		cv2.imshow('subregion', vis_roi)
         	subrects = detect(roi.copy(), nested)
            	draw_rects(vis_roi, subrects, (255, 0, 0))
	   	log = open("facefile.txt", "a")
	   	log.write("found a face")
	   	
	

		#ser.write("1")
		ser.write ('M106\n')
		ser.write ('G4 P500\n')
		ser.write('M107\n')

        	while ser.read() == 1:
			ser.read()
	    
        	#dt = clock() - t
        
        	#draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        	#cv2.imshow('facedetect', vis_roi)
        	#captured_frame_number=captured_frame_number+1
#	ser = serial.Serial('/dev/tty/usbserial', 9600)
#	ser.write ('5')

        	#cv2.imwrite("../data/saved_images/{0:d}.png".format(captured_frame_number),vis)
        	#if cv2.waitKey(30) & 0xFF == ord('q'):
            		#cap.release()
            		#cv2.destroyAllWindows()
            		#break