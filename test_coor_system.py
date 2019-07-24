from CoordinateSystem import CoordinateSystem
from ImageStitcher import ImageStitcher
import cv2
import numpy as np
import math
img1 = cv2.imread('images/Map1-rotate.png')
img2 = cv2.imread('images/Map2.png')  
h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]
img2_canvas_size = int(math.sqrt(math.pow(h2,2)+math.pow(w2,2)))

canvas = np.zeros((h1*2+img2_canvas_size,w1*2+img2_canvas_size,3), dtype=np.uint8)
canvas[h1+int((img2_canvas_size-h2)/2):h2+h1+int((img2_canvas_size-h2)/2), 
w1+int((img2_canvas_size-w2)/2):w1+w2+int((img2_canvas_size-w2)/2),
:3] = img2
canvas[:h1,:w1,:3] = img1
cv2.imshow('image',canvas)
cv2.waitKey(0)
coor_system = CoordinateSystem((len(canvas[0])/2,len(canvas)/2))

def getCornersOfImages(SHIFT):
    y_OffsetIMG2 = int((img2_canvas_size-h2)/2)
    x_OffsetIMG2 = int((img2_canvas_size-w2)/2)
    SHIFT_X,SHIFT_Y, thetha = SHIFT
    rectangle1 = [(SHIFT_X,SHIFT_Y),(w1+SHIFT_X,SHIFT_Y),(w1+SHIFT_X,h1+SHIFT_Y),(SHIFT_X,h1+SHIFT_Y)]
    rectangle2 = [(w1+x_OffsetIMG2,h1+y_OffsetIMG2),(w1+x_OffsetIMG2+w2,h1+y_OffsetIMG2),
    (w1+x_OffsetIMG2+w2,h1+y_OffsetIMG2+h2),(w1+x_OffsetIMG2,h1+y_OffsetIMG2+h2)]
    return rectangle1,rectangle2

rectangles = getCornersOfImages((272,61,281))
print(rectangles)
coor_system.set_rectangles(rectangles)
num = coor_system.get_indecies_on_rotate(272,61,281)

st = ImageStitcher(img1,img2,False)
st.drawImage(272,61,360-281,0)
st.set_canvas()
print(st.calculateLoss((272,61,281)))
#print(st.calculateLoss((92,92,45)))
print(num[1][0])
canvas[num[0][:]] = 240
canvas[num[1][:]] = 240
cv2.imshow('images',canvas)
cv2.waitKey(0)