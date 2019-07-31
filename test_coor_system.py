from ImageStitcher import ImageStitcher
import cv2

img1 = cv2.imread('images/Map1-rotate.png')
img2 = cv2.imread('images/Map2.png')  

# x0 = [0.5,0.5,0.2,0.2,-0.08,0.25,0.47,0.5,0.5,0,0,0,0,0]
x0 = [1,1,0,0,91,111,192,1,1,0,0,0,0,0]

stitcher =ImageStitcher(img1,img2,False)
stitcher.set_canvas()
stitcher.test_one_iter(x0)
stitcher.drawImage(x0,0)
