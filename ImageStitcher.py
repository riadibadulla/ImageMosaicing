import cv2
import numpy as np
import time 
from scipy.optimize import minimize
import random

class ImageStitcher:
    img1 = None
    img2 = None
    h1,h2,w1,w2 = 0,0,0,0
    BestX = 1
    BestY = 1

    def __init__(self, img1, img2, resize):
        self.img1 = img1
        self.img2 = img2
        if (resize):
            self.img1 = cv2.resize(self.img1,None,fx=0.1,fy=0.1)
            self.img2 = cv2.resize(self.img2,None,fx=0.1,fy=0.1)
        self.h1, self.w1 = self.img1.shape[:2]
        self.h2, self.w2 = self.img2.shape[:2]
        print("H1: ",self.h1,"  W1: ",self.w1,"\nH2: ",self.h2,"  W2: ",self.w2)
        

    def getIntersectionCoordinates(self,h1,w1,h2,w2,SHIFT_X,SHIFT_Y):
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

    def calculateLoss(self,SHIFT):
        SHIFT_X,SHIFT_Y = SHIFT
        SHIFT_X, SHIFT_Y = int(SHIFT_X*(self.w1+self.w2)),int(SHIFT_Y*(self.h1+self.h2))
        print("SHIFT_X: ",SHIFT_X,"    SHIFT_Y: ",SHIFT_Y)
        if (SHIFT_X>=self.w1+self.w2 or SHIFT_Y>=self.h1+self.h2 or SHIFT_Y<1 or SHIFT_X<1):
            return 255*3*self.w1*self.h1*self.h2*self.w2
        canvas = np.zeros((self.h1*2+self.h2,self.w1*2+self.w2,3), dtype=np.uint8)
        canvas[:self.h1,:self.w1,:3] = self.img1
        canvas[self.h1:self.h2+self.h1, self.w1:self.w1+self.w2,:3] = self.img2

        coor = self.getIntersectionCoordinates(self.h1,self.w1,self.h2,self.w2,SHIFT_X,SHIFT_Y)
        image1 = canvas[coor['y6']-SHIFT_Y:coor['y5']-SHIFT_Y,coor['x5']-SHIFT_X:coor['x6']-SHIFT_X,:3]
        image2 = canvas[coor['y6']:coor['y5'],coor['x5']:coor['x6'],:3]
        loss = np.mean(np.absolute(np.subtract(image1,image2)))
        return loss

    def drawImage(self,X,Y):
        vis = np.zeros((self.h1*2+self.h2,self.w1*2+self.w2,3), dtype=np.uint8)
        vis[Y:self.h1+Y,X:self.w1+X,:3] = self.img1
        vis[self.h1:self.h2+self.h1, self.w1:self.w1+self.w2,:3] = self.img2
        cv2.imwrite("output.jpg",vis)
        cv2.imshow('image',vis)
        cv2.waitKey(500)


    def mosaicImages(self):
        savedParameters = [[],[]]
        SHIFT_X = 1
        SHIFT_Y = 1
        for i in range(100):
            x = random.uniform(0,1)
            y = random.uniform(0,1)
            print("Initial Values: ",x,"  ",y)
            x0 = [x,y]
            res = minimize(self.calculateLoss,x0, method = 'nelder-mead', options={'disp':True})
            savedParameters[0].append(res.fun)
            savedParameters[1].append(res.x)
            print("\n\n\n\n")
        
        minimumErrorIndex = savedParameters[0].index(min(savedParameters[0]))
        print("\n\n\n\n\n\n")
        print(minimumErrorIndex)
        print(savedParameters[0][minimumErrorIndex])
        print(savedParameters[1][minimumErrorIndex][0]*(self.w1+self.w2))
        print(savedParameters[1][minimumErrorIndex][1]*(self.w1+self.w2))
        self.BestX, self.BestY = int(savedParameters[1][minimumErrorIndex][0]*(self.w1+self.w2)),int(savedParameters[1][minimumErrorIndex][1]*(self.h1+self.h2))
        

        


