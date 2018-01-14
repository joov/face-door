import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,100,apertureSize = 3)

cv2.imwrite(sys.argv[1][:sys.argv[1].find('.jpg')]+'_edges.jpg' ,edges)

lines = cv2.HoughLines(edges,2,np.pi/180,300)

width, height, channels = img.shape
max = max(width, height)


print('lines found ', len(lines))

angles = list(map(lambda x: x[0][1], lines))

ms = MeanShift()
ms.fit(angles)

print('Clusters found ', len(ms.cluster_centers_))

for line in lines:
	for rho,theta in line:
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 2*max*(-b))
		y1 = int(y0 + 2*max*(a))
		x2 = int(x0 - 2*max*(-b))
		y2 = int(y0 - 2*max*(a))

		cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imwrite(sys.argv[1][:sys.argv[1].find('.jpg')]+'_w_lines.jpg' ,img)