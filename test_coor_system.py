from ImageStitcher import ImageStitcher
import cv2

img1 = cv2.imread('images/island.jpg')
img2 = cv2.imread('images/island2.jpg')  

x0 = [-0.25,-0.25,0,0,0,0.501, 0.3614,-0.25,-0.25,0,0,0,0,0]
# x0 = [-0.25, -0.25, 0.17014250497314776, 0.4378971774634577, 0, 0.3631554746160932, 0.42378292326820755, -0.25, -0.25, 0.3658500688844794, 0.3506367422975808, 0, 0.06394339183165745, 0.064925597015935]
x0 = [-0.25, -0.25, 0, 0, 0, 0.5464312371352942, 0.5089438150779929, -0.25, -0.25, 0, 0, 0, 0.04239561891066475, 0.14828700959412922]
stitcher =ImageStitcher(img1,img2,False)
stitcher.set_canvas()
stitcher.test_one_iter(x0)
stitcher.drawImage(x0,0)
