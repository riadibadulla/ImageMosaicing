import cv2
import numpy as np
import time 
from ImageStitcher import ImageStitcher
import os
import sys

class main:

    def mosaic2Images(img1,img2,iterations):
        START_TIME = time.time()
        mosaic = ImageStitcher(img1.copy(),img2.copy(),True)
        mosaic.mosaicImages(iterations)
        END_TIME = time.time()
        print("Time taken: ", format(END_TIME - START_TIME), " seconds")
        mosaic.drawImage(mosaic.best_parameters,0)

    def clearScreen():
        os.system('clear')

    if __name__=='__main__':
        clearScreen()
        arguments = sys.argv
        image1_name = 'images/' + arguments[1]
        image2_name = 'images/' + arguments[2]
        number_of_iterations = int(arguments[3])
        img1 = cv2.imread(image1_name)
        img2 = cv2.imread(image2_name)  
        print("Starting the algorithm\n\n")
        mosaic2Images(img1,img2,number_of_iterations)