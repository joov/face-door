import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,100,apertureSize = 3)
minLineLength = 500
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for line in lines:
	for x1,y1,x2,y2 in line:
		cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imwrite(sys.argv[1][:sys.argv[1].find('.jpg')]+'_w_lines_fast.jpg' ,img)