import cv2
import numpy as np
import sys
from sklearn.cluster import MeanShift
import imutils
from picamera import PiCamera


SIZE_X=736
SIZE_Y=480

camera = PiCamera()
output = np.empty((SIZE_Y, SIZE_X, 3), dtype=np.uint8)

while True:
	camera.capture(output, format="bgr")

	# img = cv2.imread(sys.argv[1])

	# rotate image
	img = imutils.rotate(output, -90)

	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,50,100,apertureSize = 3)

	cv2.imwrite(sys.argv[1][:sys.argv[1].find('.jpg')]+'_edges.jpg' ,edges)

	lines = cv2.HoughLines(edges,1,np.pi/180,100)

	width, height, channels = img.shape
	maxlen = max(width, height)


	print('lines found ', len(lines))

	print ('lines')
	print (np.asarray(lines))

	#angles = list(map(lambda x: x[0][1], lines))

	ms = MeanShift()
	#ms.fit(np.asarray(angles).reshape(-1,1))

	print("transformed")
	print (np.asarray(lines).reshape(-1,2))
	ms.fit(np.asarray(lines).reshape(-1,2))

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