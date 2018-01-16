#!/usr/bin/python3
import cv2
import numpy as np
import sys
from sklearn.cluster import MeanShift
from sklearn import preprocessing
import imutils
from picamera import PiCamera
import yaml

SIZE_X=736
SIZE_Y=480
ROTATION = 0


def movement(mat_1,mat_2):
    mat_1_gray     = cv2.cvtColor(mat_1.copy(),cv2.COLOR_BGR2GRAY)
    mat_1_gray     = cv2.blur(mat_1_gray,(blur1,blur1))
    _,mat_1_gray   = cv2.threshold(mat_1_gray,100,255,0)
    mat_2_gray     = cv2.cvtColor(mat_2.copy(),cv2.COLOR_BGR2GRAY)
    mat_2_gray     = cv2.blur(mat_2_gray,(blur1,blur1))
    _,mat_2_gray   = cv2.threshold(mat_2_gray,100,255,0)
    mat_2_gray     = cv2.bitwise_xor(mat_1_gray,mat_2_gray)
    mat_2_gray     = cv2.blur(mat_2_gray,(blur2,blur2))
    _,mat_2_gray   = cv2.threshold(mat_2_gray,70,255,0)
    mat_2_gray     = cv2.erode(mat_2_gray,np.ones((erodeval,erodeval)))
    mat_2_gray     = cv2.dilate(mat_2_gray,np.ones((4,4)))
    _, contours,__ = cv2.findContours(mat_2_gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
	    #If there were any movements
	   return mat_2_gray 
    #if not
    return  None                    

with open('config.yml', 'r') as stream:
	params = yaml.load(stream)
	if 'height' in params:
		SIZE_X = params['height']
		print ("Height found ", SIZE_X)
	if 'width' in params:
		SIZE_Y = params['width']

	if 'rotation' in params:
		ROTATION = params['rotation']





camera = PiCamera()
output = np.empty((SIZE_Y, SIZE_X, 3), dtype=np.uint8)

sigma = 0.33
last_img = None

while True:
	camera.capture(output, format="bgr")

	# img = cv2.imread(sys.argv[1])

	# rotate image
	img = imutils.rotate(output, ROTATION)


	if last_img is None:
		last_img = img.copy()
		continue


	delta = movement(img, last_img) 
	if delta is None:
		continue


	width, height, channels = delta.shape
	maxlen = max(width, height)


	v = np.median(delta)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))

	edges = cv2.Canny(delta,lower, upper)

	
	cv2.imwrite(sys.argv[1][:sys.argv[1].find('.jpg')]+'_edges.jpg' ,edges)

	try:
		lines = cv2.HoughLines(delta,1,np.pi/180,160)
		print('found valid delta-image')
	except:
		continue



	print('lines found ', len(lines))

#	print ('lines')
	line_array = preprocessing.scale(np.asarray(lines).reshape(-1,2))
#	print (line_array)

	#angles = list(map(lambda x: x[0][1], lines))

	ms = MeanShift()
	#ms.fit(np.asarray(angles).reshape(-1,1))

#	print("transformed")
#	print (line_array)
	ms.fit(line_array)

	print('Clusters found ', len(ms.cluster_centers_))

	for line in lines:
		for rho,theta in line:
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 2*maxlen*(-b))
			y1 = int(y0 + 2*maxlen*(a))
			x2 = int(x0 - 2*maxlen*(-b))
			y2 = int(y0 - 2*maxlen*(a))

			cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

	cv2.imwrite(sys.argv[1][:sys.argv[1].find('.jpg')]+'_w_lines.jpg' ,img)

	last_img = img.copy()