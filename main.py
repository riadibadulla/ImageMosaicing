import cv2
import numpy as np
import time 
from ImageStitcher import ImageStitcher

class main:

    def mosaic2Images(img1,img2):
        mosaic = ImageStitcher(img1.copy(),img2.copy(),False)
        mosaic.mosaicImages(20)
        mosaic.drawImage(mosaic.BestX,mosaic.BestY,360-mosaic.Best_Rotate,0)

    if __name__=='__main__':
        START_TIME = time.time()
        img1 = cv2.imread('images/Map1-rotate.png')
        img2 = cv2.imread('images/Map2.png')  
        mosaic2Images(img1,img2)
        END_TIME = time.time()
        print("Time taken: ", format(END_TIME - START_TIME), " seconds")