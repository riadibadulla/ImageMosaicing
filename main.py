import cv2
import numpy as np
import time 
import ImageStitcher

START_TIME = time.time()

img1 = cv2.imread('/cs/home/ri31/project-scripts/canvasWithPictures/images/file.jpg')
img2 = cv2.imread('/cs/home/ri31/project-scripts/canvasWithPictures/images/file1.jpg')  

mosaic = ImageStitcher(img1,img2,True)
mosaic.mosaicImages()
mosaic.drawImage(mosaic.BestX,mosaic.BestY)

END_TIME = time.time()
print("Time taken: ", format(END_TIME - START_TIME), " seconds")