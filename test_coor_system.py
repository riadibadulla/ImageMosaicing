from CoordinateSystem import CoordinateSystem
from ImageStitcher import ImageStitcher
import cv2
import numpy as np
import math
img1 = cv2.imread('images/Map1-rotate.png')
img2 = cv2.imread('images/Map2.png')  

x0 = [1,2,2,1,0,120,100,1,1,1,1,-45,0,0]
stitcher =ImageStitcher(img1,img2,False)
stitcher.test_one_iter(x0)