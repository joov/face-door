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
    mat_1_gray     = cv2.blur(mat_1_gray,(4,4))
    _,mat_1_gray   = cv2.threshold(mat_1_gray,100,255,0)

    mat_2_gray     = cv2.cvtColor(mat_2.copy(),cv2.COLOR_BGR2GRAY)
    mat_2_gray     = cv2.blur(mat_2_gray,(4,4))
    _,mat_2_gray   = cv2.threshold(mat_2_gray,100,255,0)

    mat_2_gray     = cv2.bitwise_xor(mat_1_gray,mat_2_gray)
    mat_2_gray     = cv2.erode(mat_2_gray,np.ones((4,4)))
    mat_2_gray     = cv2.dilate(mat_2_gray,np.ones((4,4)))

    return mat_2_gray 

with open('config.yml', 'r') as stream:
    params = yaml.load(stream)
    if 'height' in params:
        SIZE_X = params['height']
        print ("Height found ", SIZE_X)
    if 'width' in params:
        SIZE_Y = params['width']

    if 'rotation' in params:
        ROTATION = params['rotation']


img1 = cv2.imread('closed.jpg', cv2.IMREAD_UNCHANGED)
img2 = cv2.imread('open.jpg', cv2.IMREAD_UNCHANGED)


# rotate image
img1 = imutils.rotate(img1, ROTATION)
img2 = imutils.rotate(img2, ROTATION)


delta = movement(img1, img2)
cv2.imwrite('delta.jpg', delta)

width, height = delta.shape
maxlen = max(width, height)


# apply automatic Canny edge detection using the computed median

edges = cv2.Canny(delta,240, 250)


cv2.imwrite('delta_edges.jpg', edges)

try:
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
    print('found valid delta-image with lines', len(lines))
except:
    print('No lines found')
    quit()

line_array = preprocessing.scale(np.asarray(lines).reshape(-1, 2))
#    print (line_array)

#angles = list(map(lambda x: x[0][1], lines))

#ms = MeanShift()
#ms.fit(np.asarray(angles).reshape(-1,1))

#    print("transformed")
#    print (line_array)
# ms.fit(line_array)

#    print('Clusters found ', len(ms.cluster_centers_))

for line in lines:
    for rho, theta in line:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 2*maxlen*(-b))
        y1 = int(y0 + 2*maxlen*(a))
        x2 = int(x0 - 2*maxlen*(-b))
        y2 = int(y0 - 2*maxlen*(a))

        cv2.line(img2, (x1 ,y1), (x2, y2),(0, 0, 255), 2)

cv2.imwrite('delta_w_lines.jpg', img2)
