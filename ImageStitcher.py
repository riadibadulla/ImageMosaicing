import cv2
import numpy as np
import time 

class ImageStitcher:
    img1 = None
    img2 = None
    h1,h2,w1,w2 = 0
    BestX = 1
    BestY = 1

    def __init__(self, img1, im2, resize):
        self.img1 = img1
        self.img2 = img2
        if (resize):
            self.img1 = cv2.resize(self.img1,None,fx=0.1,fy=0.1)
            self.img2 = cv2.resize(self.img2,None,fx=0.1,fy=0.1)
        h1, w1 = self.img1.shape[:2]
        h2, w2 = self.img2.shape[:2]
        

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
        return {'x5':x5,'y5':y5,'x6':x6,'y6':y6}

    def calculateLoss(canvas, SHIFT_X,SHIFT_Y,h1,w1,h2,w2):
        coor = getIntersectionCoordinates(h1,w1,h2,w2,SHIFT_X,SHIFT_Y)
        image1 = canvas[coor['y6']-SHIFT_Y:coor['y5']-SHIFT_Y,coor['x5']-SHIFT_X:coor['x6']-SHIFT_X,:3]
        image2 = canvas[coor['y6']:coor['y5'],coor['x5']:coor['x6'],:3]
        loss = np.mean(np.absolute(np.subtract(image1,image2)))
        return loss

    def drawImage(X,Y):
        vis = np.zeros((h1*2+h2,w1*2+w2,3), dtype=np.uint8)
        vis[Y:h1+Y,X:w1+X,:3] = img1
        vis[h1:h2+h1, w1:w1+w2,:3] = img2
        cv2.imwrite("output.jpg",vis)
        cv2.imshow('image',vis)
        cv2.waitKey(500)


    def mosaicImages(self):
        SHIFT_X = 1
        SHIFT_Y = 1

        canvas = np.zeros((h1*2+h2,w1*2+w2,3), dtype=np.uint8)
        canvas[:h1,:w1,:3] = img1
        canvas[h1:h2+h1, w1:w1+w2,:3] = img2

        BestLoss = calculateLoss(canvas,SHIFT_X,SHIFT_Y,self.h1,self.w1,self.h2,self.w2)
        SHIFT_Y=2
        while(SHIFT_X<self.w1+self.w2):
            print("SHIFTX:",SHIFT_X)
            #drawImage(SHIFT_X,SHIFT_Y)
            while(SHIFT_Y<self.h1+self.h2):
                loss = calculateLoss(canvas,SHIFT_X,SHIFT_Y,self.h1,self.w1,self.h2,self.w2)
                #drawImage(SHIFT_X,SHIFT_Y)
                print("LOSS: ",loss,"BestLoss: ",BestLoss)
                if loss<BestLoss:
                    drawImage(SHIFT_X,SHIFT_Y)
                    BestLoss = loss
                    BestX = SHIFT_X
                    BestY = SHIFT_Y
                SHIFT_Y+=1
            SHIFT_Y = 1
            SHIFT_X+=1


