import cv2
import numpy as np
import time 

def getIntersectionCoordinates(h1,w1,h2,w2,SHIFT_X,SHIFT_Y):
    x1 = w1
    x2 = w1+w2
    y1 = h1+h2
    y2 = h1
    x3=SHIFT_X
    y3=SHIFT_Y+h1
    x4 = SHIFT_X+w1
    y4=SHIFT_Y

    x5 = max(x1, x3) 
    y5 = min(y1, y3) 
    x6 = min(x2, x4) 
    y6 = max(y2, y4) 
    # if (x5 > x6 or y5 > y6) : 
    #     print("No intersection") 
    #     return
    return (x5,y5,x6,y6)

def calculateLoss(canvas, SHIFT_X,SHIFT_Y,h1,w1,h2,w2):
    coor = getIntersectionCoordinates(h1,w1,h2,w2,SHIFT_X,SHIFT_Y)
    image1 = canvas[0,coor[3]:coor[1],coor[0]:coor[2],:3]
    image2 = canvas[1,coor[3]:coor[1],coor[0]:coor[2],:3]
    loss = np.mean(np.absolute(np.subtract(image1,image2)))
    return loss

def drawImage(X,Y):
    vis = np.zeros((h1*2+h2,w1*2+w2,3), dtype=np.uint8)
    vis[Y:h1+Y,X:w1+X,:3] = img1
    vis[h1:h2+h1, w1:w1+w2,:3] = img2
    cv2.imshow('image',vis)
    cv2.waitKey(10)

START_TIME = time.time()



img1 = cv2.imread('/cs/home/ri31/project-scripts/canvasWithPictures/images/Map1.png')
img2 = cv2.imread('/cs/home/ri31/project-scripts/canvasWithPictures/images/Map2.png')  

h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]

SHIFT_X = 1
SHIFT_Y = 1

canvas = np.zeros((2,h1*2+h2,w1*2+w2,3), dtype=np.uint8)
canvas[0,:h1,:w1,:3] = img1
canvas[1,h1:h2+h1, w1:w1+w2,:3] = img2

BestLoss = calculateLoss(canvas,SHIFT_X,SHIFT_Y,h1,w1,h2,w2)
SHIFT_Y=2
BestX = 1
BestY = 1

while(SHIFT_X<w1+w2):
    print(SHIFT_X)
    #drawImage(SHIFT_X,SHIFT_Y)
    while(SHIFT_Y<h1+h2):
        loss = calculateLoss(canvas,SHIFT_X,SHIFT_Y,h1,w1,h2,w2)
        print(SHIFT_X)
        if loss<BestLoss:
            #drawImage(SHIFT_X,SHIFT_Y)
            BestLoss = loss
            BestX = SHIFT_X
            BestY = SHIFT_Y
        SHIFT_Y+=1
        canvas[0].fill(0)
        canvas[0,SHIFT_Y:h1+SHIFT_Y,SHIFT_X:w1+SHIFT_X,:3] = img1
    SHIFT_Y = 0
    SHIFT_X+=1
    canvas[0].fill(0)
    canvas[0,SHIFT_Y:h1+SHIFT_Y,SHIFT_X:w1+SHIFT_X,:3] = img1


vis = np.zeros((h1*2+h2,w1*2+w2,3), dtype=np.uint8)
vis[BestY:h1+BestY,BestX:w1+BestX,:3] = img1
vis[h1:h2+h1, w1:w1+w2,:3] = img2
cv2.imshow('image',vis)
END_TIME = time.time()
print("Time taken: ", format(END_TIME - START_TIME), " seconds")
cv2.waitKey()