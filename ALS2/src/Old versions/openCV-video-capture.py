# from http://picamera.readthedocs.org/en/release-1.8/recipes1.html#capturing-to-an-opencv-object


import io
import time
import picamera
import cv2
import cv2.cv as cv
import numpy as np


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        



# Create the in-memory stream
stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(2)
    camera.capture(stream, format='jpeg')
# Construct a numpy array from the stream
data = np.fromstring(stream.getvalue(), dtype=np.uint8)
# "Decode" the image from the array, preserving colour
image = cv2.imdecode(data, 1)
# OpenCV returns an array with data in BGR order. If you want RGB instead
# use the following...
# image = image[:, :, ::-1]



cascade_fn = "../data/haarcascades/haarcascade_frontalface_alt.xml"
nested_fn  = "../data/haarcascades/haarcascade_eye.xml"

cascade = cv2.CascadeClassifier(cascade_fn)
nested = cv2.CascadeClassifier(nested_fn)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)

rects = detect(gray, cascade)

vis = image.copy() ##??????
draw_rects(vis, rects, (0, 255, 0))
for x1, y1, x2, y2 in rects:
    roi = gray[y1:y2, x1:x2]
    vis_roi = vis[y1:y2, x1:x2]
    cv2.imshow('subregion', vis_roi)
    subrects = detect(roi.copy(), nested)
    draw_rects(vis_roi, subrects, (255, 0, 0))

# cv2.imshow('facedetect', vis)

while(True):
	if cv2.waitKey(30) & 0xFF == ord('q'):
		# cap.release()
		cv2.destroyAllWindows()
		break

