#import cv2
#import cv
#import time
#from facedetect import *
#import sys, getopt
import cv2
import cv2.cv as cv
from video import create_capture
from common import clock, draw_str
import sys
import getopt
#from Arduino import Arduino
import picamera
import numpy as np


import serial

### THIS IS THE VIDEO THAT WILL BE PROCESSED
video_file_name = '../noface.mp4'


help_message = '''
USAGE: facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects
#    logfile = open("logfile.txt", "a")
 #   logfile.write("Found a face")

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        
connected = False
ser = serial.Serial("/dev/ttyACM0",9600)

#while not connected:
#	try:
#	 serin = ser.read()
#	except ValueError:
#	 continue	
#	 connected = True 


if __name__ == '__main__':
    
    

    print help_message

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    try: video_src = video_src[0]
    except: video_src = 0
    args = dict(args)
    cascade_fn = args.get('--cascade', "../data/haarcascades/haarcascade_frontalface_alt.xml")
    nested_fn  = args.get('--nested-cascade', "../data/haarcascades/haarcascade_eye.xml")

    cascade = cv2.CascadeClassifier(cascade_fn)
    nested = cv2.CascadeClassifier(nested_fn)
    
#creating in memory stream
stream = io.BytesIO()
with picamera.PiCamera() as camera:
	camera.start_preview()
	time.sleep(2)
	camera.capture(stream, format='jpeg')

#Construct a numpy array from the stream
data = np.fromstring(stream.getvalue()_, dtype=np.uint8)

# "decode" the image from teh array, preserving color
cap = cv2.imdecode(data,1)
 	


    #cap = cv2.VideoCapture.open(0)
    width= cap.get(3)
    height = cap.get(4)
    print width
    #fourcc = cv2.VideoWriter_fourcc(cv2.FFMPEG)
    #print cv2.FFMPEG
    # http://docs.opencv.org/trunk/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
    # http://note.sonots.com/SciSoftware/haartraining.html
    #http://docs.opencv.org/trunk/modules/contrib/doc/facerec/facerec_tutorial.html
    #fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    #out = cv2.VideoWriter('output.mjpg',fourcc, 20.0, (640,480))
    #out = cv2.VideoWriter('out.avi',cv2.FFMPEG('M','J','P','G'), 20, (int(width),int(height)))
    captured_frame_number = 0
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        t = clock()
        rects = detect(gray, cascade)
        vis = frame.copy()
        draw_rects(vis, rects, (0, 255, 0))
        for x1, y1, x2, y2 in rects:
            roi = gray[y1:y2, x1:x2]
            vis_roi = vis[y1:y2, x1:x2]
            cv2.imshow('subregion', vis_roi)
            subrects = detect(roi.copy(), nested)
            draw_rects(vis_roi, subrects, (255, 0, 0))
	    log = open("facefile.txt", "a")
	    log.write("found a face")
	    ser.write("1")

            while ser.read() == 1:
		ser.read()
	    
        dt = clock() - t
        
        draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        cv2.imshow('facedetect', vis)
        captured_frame_number=captured_frame_number+1
#	ser = serial.Serial('/dev/tty/usbserial', 9600)
#	ser.write ('5')

        cv2.imwrite("../data/saved_images/{0:d}.png".format(captured_frame_number),vis)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

