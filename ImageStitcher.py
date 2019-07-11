import cv2
import numpy as np
import time 
from scipy.optimize import minimize
import random
import math

class ImageStitcher:
    img1 = None
    img2 = None
    img2_canvas_size = None
    h1,h2,w1,w2 = 0,0,0,0
    BestX = 1
    BestY = 1
    Best_Rotate = 1

    def __init__(self, img1, img2, resize):
        self.img1 = img1
        self.img2 = img2
        if (resize):
            self.img1 = cv2.resize(self.img1,None,fx=0.1,fy=0.1)
            self.img2 = cv2.resize(self.img2,None,fx=0.1,fy=0.1)
        self.h1, self.w1 = self.img1.shape[:2]
        self.h2, self.w2 = self.img2.shape[:2]
        self.img2_canvas_size = int(math.sqrt(math.pow(self.h2,2)+math.pow(self.w2,2)))

        print("H1: ",self.h1,"  W1: ",self.w1,"\nH2: ",self.h2,"  W2: ",self.w2)
        
    def rotateTranslateCoordinates(self, X,Y,centreX,centreY):
        tempX = X - centreX
        tempY = Y - centreY
        rotatedX = tempX*math.cos(45 * math.pi/180) - tempY*math.sin(45 * math.pi/180)
        rotatedY = tempX*math.sin(45 * math.pi/180) + tempY*math.cos(45 * math.pi/180)
        x = rotatedX + centreX
        y = rotatedY + centreY
        return x,y

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
        SHIFT_X,SHIFT_Y, thetha = SHIFT
        SHIFT_X, SHIFT_Y, thetha = int(SHIFT_X*(self.w1+self.w2)),int(SHIFT_Y*(self.h1+self.h2)),int(thetha*360)
        print("SHIFT_X: ",SHIFT_X,"    SHIFT_Y: ",SHIFT_Y,"    Angle: ",thetha)
        if (SHIFT_X>=self.w1+self.img2_canvas_size-self.img2_canvas_size*0.05 or SHIFT_Y>=self.h1+self.img2_canvas_size-self.img2_canvas_size*0.05 or SHIFT_Y<self.img2_canvas_size*0.05 or SHIFT_X<self.img2_canvas_size*0.05):
            return 255*3*self.w1*self.h1*self.h2*self.w2
        canvas = self.rotateImage(thetha)
        canvas[:self.h1,:self.w1,:3] = self.img1
        # self.drawImage(SHIFT_X,SHIFT_Y,thetha,10)
        coor = self.getIntersectionCoordinates(self.h1,self.w1,self.img2_canvas_size,self.img2_canvas_size,SHIFT_X,SHIFT_Y)
        image1 = canvas[coor['y6']-SHIFT_Y:coor['y5']-SHIFT_Y,coor['x5']-SHIFT_X:coor['x6']-SHIFT_X,:3]
        image2 = canvas[coor['y6']:coor['y5'],coor['x5']:coor['x6'],:3]
        if np.sum(image2)==0:
            return 255*3*self.w1*self.h1*self.h2*self.w2
        difference = np.square(np.subtract(image1[np.nonzero(image2)],image2[np.nonzero(image2)]))
        loss = np.mean(difference)
        return loss

    def drawImage(self,X,Y, thetha,time):
        vis = self.rotateImage(thetha)
        vis[Y:self.h1+Y,X:self.w1+X,:3] = self.img1
        cv2.imwrite("output.jpg",vis)
        cv2.imshow('image',vis)
        cv2.waitKey(time)

    def rotateImage(self,angleInDegrees):
        thetha = angleInDegrees * math.pi/180
        a = math.cos(thetha)
        b = math.sin(thetha)
        canvas = np.zeros((self.h1*2+self.img2_canvas_size,self.w1*2+self.img2_canvas_size,3), dtype=np.uint8)
        canvas[self.h1+int((self.img2_canvas_size-self.h2)/2):self.h2+self.h1+int((self.img2_canvas_size-self.h2)/2), 
        self.w1+int((self.img2_canvas_size-self.w2)/2):self.w1+self.w2+int((self.img2_canvas_size-self.w2)/2),
        :3] = self.img2
        h, w = canvas.shape[:2]
        M = np.float32([[a,b,(1-a)*w/2-b*h/2],[-b,a,b*w/2+(1-a)*h/2],[0,0,1]])
        canvas = cv2.warpPerspective(canvas,M,(w,h))
        # canvas[:self.h1,:self.w1,:3] = self.img1
        return canvas


    def mosaicImages(self,n):
        savedParameters = [[],[]]
        intitial_cors_x = np.linspace(0.1,1,n,False)
        intitial_cors_y = np.linspace(0.1,1,n,False)
        initial_param_thetha = np.linspace(0,1,n,False)
        for i in range(n):
            thetha = initial_param_thetha[i]
            for j in range(n):
                x = intitial_cors_x[j]
                for k in range(n):
                    y = intitial_cors_y[k]
                    print("Initial Values: ",x,"  ",y)
                    x0 = [x,y,thetha]
                    res = minimize(self.calculateLoss,x0, method = 'nelder-mead', options={'disp':True})
                    savedParameters[0].append(res.fun)
                    print(res.fun)
                    savedParameters[1].append(res.x)
                    print("\n\n\n\n")
        
        minimumErrorIndex = savedParameters[0].index(min(savedParameters[0]))
        print("\n\n\n\n\n\n")
        print(savedParameters)
        print("\n\n\n\n\n\n")
        print(minimumErrorIndex)
        print(savedParameters[0][minimumErrorIndex])
        print(savedParameters[1][minimumErrorIndex][0]*(self.w1+self.w2))
        print(savedParameters[1][minimumErrorIndex][1]*(self.w1+self.w2))
        print(savedParameters[1][minimumErrorIndex][2]*360)
        self.BestX = int(savedParameters[1][minimumErrorIndex][0]*(self.w1+self.w2))
        self.BestY = int(savedParameters[1][minimumErrorIndex][1]*(self.h1+self.h2))
        self.Best_Rotate = int(savedParameters[1][minimumErrorIndex][2]*360)