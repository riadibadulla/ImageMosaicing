import cv2
import numpy as np
import math
def rotateImage(angleInDegrees,canvas):
    thetha = angleInDegrees * math.pi/180
    a = math.cos(thetha)
    b = math.sin(thetha)
    h, w = canvas.shape[:2]
    M = np.float32([[a,b,(1-a)*w/2-b*h/2],[-b,a,b*w/2+(1-a)*h/2],[0,0,1]])
    canvas = cv2.warpPerspective(canvas,M,(w,h))
    return canvas

canvas = np.zeros((50,50,3), dtype=np.uint8)
canvas[10][10]=[255,255,255]
canvas[10][20]=[255,255,255]
canvas[20][10]=[255,255,255]
canvas[20][20]=[255,255,255]
canvas2 = rotateImage(45,canvas)
cv2.imshow('image',canvas)
cv2.waitKey(0)
cv2.imshow('image',canvas2)
cv2.waitKey(0)

def rotateTranslateCoordinates(X,Y,centreX,centreY):
    tempX = X - centreX
    tempY = Y - centreY
    rotatedX = tempX*math.cos(45 * math.pi/180) - tempY*math.sin(45 * math.pi/180)
    rotatedY = tempX*math.sin(45 * math.pi/180) + tempY*math.cos(45 * math.pi/180)
    x = rotatedX + centreX
    y = rotatedY + centreY
    return x,y

canvas3 = np.zeros((50,50,3), dtype=np.uint8)
x,y = RotateTranslateCoordinates(10,10,15,15)
canvas3[int(x)][int(y)]=[255,255,255]

tempX = 20 - 15
tempY = 10 - 15
rotatedX = tempX*math.cos(45 * math.pi/180) - tempY*math.sin(45 * math.pi/180)
rotatedY = tempX*math.sin(45 * math.pi/180) + tempY*math.cos(45 * math.pi/180)
x = rotatedX + 15
y = rotatedY + 15
canvas3[int(x)][int(y)]=[255,255,255]

tempX = 10 - 15
tempY = 20 - 15
rotatedX = tempX*math.cos(45 * math.pi/180) - tempY*math.sin(45 * math.pi/180)
rotatedY = tempX*math.sin(45 * math.pi/180) + tempY*math.cos(45 * math.pi/180)
x = rotatedX + 15
y = rotatedY + 15
canvas3[int(x)][int(y)]=[255,255,255]

tempX = 20 - 15
tempY = 20 - 15
rotatedX = tempX*math.cos(45 * math.pi/180) - tempY*math.sin(45 * math.pi/180)
rotatedY = tempX*math.sin(45 * math.pi/180) + tempY*math.cos(45 * math.pi/180)
x = rotatedX + 15
y = rotatedY + 15
canvas3[int(x)][int(y)]=[255,255,255]

cv2.imshow('image',canvas3)
cv2.waitKey(0)