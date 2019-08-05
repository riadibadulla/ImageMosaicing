import cv2
import numpy as np
import math
img1 = cv2.imread('images/stMap1.png') 
h, w = img1.shape[:2]
zer= np.zeros((1000,1000,3), dtype=np.uint8)
zer[63:937,88:913,:]=img1

   
for i in range(90):
    M = cv2.getRotationMatrix2D((500,500),i,1)  
    img1 =cv2.warpAffine(img1,M,(1000,1000))

cv2.imwrite("rotated.png", img1)
