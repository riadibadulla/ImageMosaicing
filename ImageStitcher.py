import cv2
import numpy as np
import time 
from scipy.optimize import minimize
import random
import math
from CoordinateSystem import CoordinateSystem

class ImageStitcher:
    img1 = None
    img2 = None
    img2_canvas_size = None
    h1,h2,w1,w2 = 0,0,0,0
    BestX = 1
    BestY = 1
    Best_Rotate = 1
    canvas = None

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
        
    def getCornersOfImages(self,SHIFT):
        y_OffsetIMG2 = int((self.img2_canvas_size-self.h2)/2)
        x_OffsetIMG2 = int((self.img2_canvas_size-self.w2)/2)
        SHIFT_X,SHIFT_Y, thetha = SHIFT
        rectangle1 = [(SHIFT_X,SHIFT_Y),(SHIFT_X,self.h1+SHIFT_Y),(self.w1+SHIFT_X,self.h1+SHIFT_Y),(self.w1+SHIFT_X,SHIFT_Y)]
        rectangle2 = [(self.w1+x_OffsetIMG2,self.h1+x_OffsetIMG2),(self.w1+x_OffsetIMG2,self.h1+x_OffsetIMG2+self.h2),
        (self.w1+x_OffsetIMG2+self.w2,self.h1+x_OffsetIMG2),(self.w1+x_OffsetIMG2+self.w2,self.h1+x_OffsetIMG2+self.h2)]
        return rectangle1,rectangle2

    def calculateLoss(self,SHIFT):
        SHIFT_X,SHIFT_Y, thetha = SHIFT
        SHIFT_X, SHIFT_Y, thetha = int(SHIFT_X*(self.w1+self.w2)),int(SHIFT_Y*(self.h1+self.h2)),int(thetha*360)
        print("SHIFT_X: ",SHIFT_X,"    SHIFT_Y: ",SHIFT_Y,"    Angle: ",thetha)
        if (SHIFT_X>=self.w1+self.img2_canvas_size-self.img2_canvas_size*0.05 or SHIFT_Y>=self.h1+self.img2_canvas_size-self.img2_canvas_size*0.05 or SHIFT_Y<self.img2_canvas_size*0.05 or SHIFT_X<self.img2_canvas_size*0.05):
            return 255*3*self.w1*self.h1*self.h2*self.w2
        coor_system = CoordinateSystem(self.getCornersOfImages(SHIFT))
        coordinates_of_intersection = coor_system.get_indecies_on_rotate(SHIFT_X, SHIFT_Y,thetha)

        image1 = self.canvas[:self.h1,:self.w1,:3]
        image2 = self.canvas[self.h1+int((self.img2_canvas_size-self.h2)/2):self.h2+self.h1+int((self.img2_canvas_size-self.h2)/2), 
        self.w1+int((self.img2_canvas_size-self.w2)/2):self.w1+self.w2+int((self.img2_canvas_size-self.w2)/2),
        :3]

        difference = np.square(np.subtract(image1[coordinates_of_intersection[0]],image2[coordinates_of_intersection[1]]))
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
        self.canvas = np.zeros((self.h1*2+self.img2_canvas_size,self.w1*2+self.img2_canvas_size,3), dtype=np.uint8)
        self.canvas[self.h1+int((self.img2_canvas_size-self.h2)/2):self.h2+self.h1+int((self.img2_canvas_size-self.h2)/2), 
        self.w1+int((self.img2_canvas_size-self.w2)/2):self.w1+self.w2+int((self.img2_canvas_size-self.w2)/2),
        :3] = self.img2
        self.canvas[:self.h1,:self.w1,:3] = self.img1

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