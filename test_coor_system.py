from ImageStitcher import ImageStitcher
import cv2

img1 = cv2.imread('images/AndrewsMap1.png')
img2 = cv2.imread('images/AndrewsMap2.png')  

x0 = [0.5,0.5,0,0,0,0,0,0.5,0.5,0,0,0,0,0]


stitcher =ImageStitcher(img1,img2,False)
stitcher.set_canvas()
stitcher.test_one_iter(x0)
stitcher.drawImage(x0,0)
