import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import math

ANGLE = 47

img = cv2.imread('bella.jpg',1)
print(type(img))
rows,cols = img.shape[:2]

thetha = ANGLE * math.pi/180

a = math.cos(thetha)
b = math.sin(thetha)


M = np.float32([[a,b,(1-a)*cols/2-b*rows/2],[-b,a,b*cols/2+(1-a)*rows/2],[0,0,1]])
#M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
#dst = cv2.warpAffine(img,M,(cols,rows))
dst = cv2.warpPerspective(img,M,(cols*2,rows*2))

cv2.imshow('image',dst)
cv2.waitKey(0)