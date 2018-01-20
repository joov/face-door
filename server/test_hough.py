#!/usr/bin/python3
import cv2
import numpy as np
import sys, time
from sklearn.cluster import MeanShift
from sklearn import preprocessing
import imutils
from picamera import PiCamera
import yaml

SIZE_X=736
SIZE_Y=480
ROTATION = 0

mat_1 = None
def movement(mat_2):
    global mat_1
    if mat_1 is None:
        mat_1 = mat_2.copy()
        return

    mat_1_gray     = cv2.cvtColor(mat_1.copy(),cv2.COLOR_BGR2GRAY)
    mat_1_gray     = cv2.blur(mat_1_gray,(4,4))
    _,mat_1_gray   = cv2.threshold(mat_1_gray,100,255,0)

    mat_2_gray     = cv2.cvtColor(mat_2.copy(),cv2.COLOR_BGR2GRAY)
    mat_2_gray     = cv2.blur(mat_2_gray,(4,4))
    _,mat_2_gray   = cv2.threshold(mat_2_gray,100,255,0)

    mat_2_gray     = cv2.bitwise_xor(mat_1_gray,mat_2_gray)
    mat_2_gray     = cv2.erode(mat_2_gray,np.ones((4,4)))
    mat_2_gray     = cv2.dilate(mat_2_gray,np.ones((4,4)))

    mat_1 = mat_2.copy()

    return mat_2_gray

def get_lines(delta):

    cv2.imwrite('delta.jpg', delta)

    width, height = delta.shape
    maxlen = max(width, height)


    # apply Canny edge detection
    edges = cv2.Canny(delta,240, 250)

    cv2.imwrite('delta_edges.jpg', edges)

    try:
        lines = cv2.HoughLines(edges, 1, np.pi/180, 160)
        print('found valid delta-image with lines', len(lines))
        return lines
    except:
        print('No lines found')
        return []

def image_with_lines(img, lines):
    width, height, channels = img.shape
    maxlen = max(width, height)

    print('lines found ', len(lines))

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

            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imwrite('delta_w_lines.jpg' ,img)


### Start of main section ###########
with open('config.yml', 'r') as stream:
    params = yaml.load(stream)
    if 'height' in params:
        SIZE_X = params['width']
        print ("Width found ", SIZE_X)
    if 'width' in params:
        SIZE_Y = params['height']
        print ("Height found ", SIZE_Y)

    if 'rotation' in params:
        ROTATION = params['rotation']
        print("Rotation found", ROTATION)

camera = PiCamera()
output = np.empty((SIZE_Y, SIZE_X, 3), dtype=np.uint8)


while True:
    #time.sleep(15)
    camera.capture(output, format="bgr")

    # rotate image
    img = imutils.rotate(output, ROTATION)
    cv2.imwrite('base.jpg' ,img)

    delta = movement(img) 
    if delta is None:
        continue

    lines = get_lines(delta)
    if len(lines) == 0:
        continue

    image_with_lines(img, lines)

