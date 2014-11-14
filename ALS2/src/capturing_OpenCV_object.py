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

face_cascade = cv2.CascadeClassifier('../data/haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier('../data/haarcascade_eye.xml')

connected = False
ser = serial.Serial("/dev/ttyACM0",9600)

while True:
	camera.resolution = (640,480)
	camera.capture('image.png', format='png')
#time.sleep(10)

#Construct a numpy array from the stream
#	data = np.fromstring(stream.getvalue(), dtype=np.uint8)

# "decode" the image from teh array, preserving color
    	img = cv2.imread('image.png')
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imwrite('test2.png', img)
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
    
   	#while(cap.isOpened()):
        	#ret, frame = cap.read()
        	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        	#gray = cv2.equalizeHist(gray)

        	#t = clock()
        	#rects = detect(gray, cascade)
        	#vis = frame.copy()
        	#draw_rects(vis, rects, (0, 255, 0))
        	#for x1, y1, x2, y2 in rects:
            	#	roi = gray[y1:y2, x1:x2]
            	#	vis_roi = vis[y1:y2, x1:x2]
            	#	cv2.imshow('subregion', vis_roi)
           	#	subrects = detect(roi.copy(), nested)
            	#	draw_rects(vis_roi, subrects, (255, 0, 0))
	   	#	log = open("facefile.txt", "a")
	   	#	log.write("found a face")
	   	
	faces = face_cascade.detectMultiScale(gray,1.3,5)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		eyes = eye_cascade.detectMultiScale(roi_gray)
		for (ex, ey, ew, eh) in eyes:
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

	#cv2.imshow('img', img)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	#ser.write("1")
			ser.write ('M106\n')
			ser.write ('G4 S1\n')
			ser.write('M107\n')

        		while ser.read() == 1:
				ser.read()
	    
        	#dt = clock() - t
        
        	#draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        	#cv2.imshow('facedetect', vis)
        	#captured_frame_number=captured_frame_number+1
#	ser = serial.Serial('/dev/tty/usbserial', 9600)
#	ser.write ('5')

        	#cv2.imwrite("../data/saved_images/{0:d}.png".format(captured_frame_number),vis)
        	#if cv2.waitKey(30) & 0xFF == ord('q'):
            		#cap.release()
            		#cv2.destroyAllWindows()
            		#break