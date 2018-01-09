import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,100,apertureSize = 3)

cv2.imwrite(sys.argv[1][:sys.argv[1].find('.jpg')]+'_edges.jpg' ,edges)

lines = cv2.HoughLines(edges,2,np.pi/180,100)

print('lines found ', len(lines))
for rho,theta in lines:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imwrite(sys.argv[1][:sys.argv[1].find('.jpg')]+'_w_lines.jpg' ,img)