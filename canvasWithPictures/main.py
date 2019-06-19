import cv2
import numpy as np


SHIFT_CONST = 500

img1 = cv2.imread('/cs/home/ri31/project-scripts/canvasWithPictures/images/andrews1.png')
img2 = cv2.imread('/cs/home/ri31/project-scripts/canvasWithPictures/images/andrews2.png')  

h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]

vis = np.zeros((max(h1, h2), w1+w2,3), np.uint8)
vis[:h1, :w1,:3] = img1
vis[:h2, w1-SHIFT_CONST:w1+w2-SHIFT_CONST,:3] = img2

cv2.imshow('image',vis)
cv2.waitKey()