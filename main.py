import cv2
import numpy as np
import time 
from ImageStitcher import ImageStitcher
import os

class main:

    def mosaic2Images(img1,img2):
        mosaic = ImageStitcher(img1.copy(),img2.copy(),False)
        mosaic.mosaicImages(1500)
        mosaic.drawImage(mosaic.BestX,mosaic.BestY,360-mosaic.Best_Rotate,0)

    def clearScreen():
        os.system('clear')

    if __name__=='__main__':
        START_TIME = time.time()
        clearScreen()
        img1 = cv2.imread('images/andrews1.png')
        img2 = cv2.imread('images/andrews2.png')  
        print("Starting the algorithm\n\n")
        mosaic2Images(img1,img2)
        END_TIME = time.time()
        print("Time taken: ", format(END_TIME - START_TIME), " seconds")