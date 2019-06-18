import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

img = cv2.imread('bella.jpg',0)
print(type(img))
rows,cols = img.shape

M = np.float32([[1,0,10],[0,1,60]])
dst = cv2.warpAffine(img,M,(cols,rows))
#dst = cv2.warpPerspective(img,M,(cols,rows))


cv2.imshow('frame1',dst)
cv2.imshow('frame2',img)
cv2.waitKey(0)
cv2.destroyAllWindows()