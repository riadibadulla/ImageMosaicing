import cv2
import numpy as np
# import time 
from scipy.optimize import minimize
import random
import math
from CoordinateSystem import CoordinateSystem
import random
import sys
from joblib import Parallel, delayed

class ImageStitcher:
    img1 = None
    img2 = None
    img2_canvas_size = None
    h1,h2,w1,w2 = 0,0,0,0
    BestX = 1
    BestY = 1
    Best_Rotate = 1
    canvas = None
    coor_system = None

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
        
    def getCornersOfImages(self):
        y_OffsetIMG2 = int((self.img2_canvas_size-self.h2)/2)
        x_OffsetIMG2 = int((self.img2_canvas_size-self.w2)/2)
        rectangle1 = [(0,0),(0,self.h1),(self.w1,self.h1),(self.w1,0)]
        rectangle2 = [(self.w1+x_OffsetIMG2,self.h1+y_OffsetIMG2),(self.w1+x_OffsetIMG2,self.h1+y_OffsetIMG2+self.h2),
        (self.w1+x_OffsetIMG2+self.w2,self.h1+y_OffsetIMG2+self.h2),(self.w1+x_OffsetIMG2+self.w2,self.h1+y_OffsetIMG2)]
        return rectangle1,rectangle2

    def calculateLoss(self,parameters):
        # SHIFT_X, SHIFT_Y, thetha = int(SHIFT_X),int(SHIFT_Y),int(thetha)
        self.coor_system.set_rectangles(self.getCornersOfImages())
        self.coor_system.set_canvas(self.canvas.shape[:2])
        coordinates_of_intersection = self.coor_system.get_indecies_on_rotate(parameters)
        if (coordinates_of_intersection == -1):
            return 255*3*self.w1*self.h1*self.h2*self.w2
        difference = np.square(np.subtract(self.canvas[coordinates_of_intersection[0]],self.canvas[coordinates_of_intersection[1]]))
        loss = np.mean(difference)
        #sys.stdout.write("\rLoss:{3}       ☚||||".format(loss))
        print(loss)
        return loss

    def drawImage(self,param,time):
        a,b,c,d,thetha,t_x,t_y, a1,b1,c1,d1,thetha1,t_x1,t_y1 = param
        thetha = thetha * math.pi/180
        thetha1 = thetha1 * math.pi/180
        r_cos = math.cos(thetha)
        r_sin = math.sin(thetha)
        r_cos1 = math.cos(thetha1)
        r_sin1 = math.sin(thetha1)
        centrex = self.w1/2
        centrey = self.h1/2

        vis1 = np.zeros((self.h1*2+self.img2_canvas_size,self.w1*2+self.img2_canvas_size,3), dtype=np.uint8)
        vis2 = np.zeros((self.h1*2+self.img2_canvas_size,self.w1*2+self.img2_canvas_size,3), dtype=np.uint8)
        vis2[self.h1+int((self.img2_canvas_size-self.h2)/2):self.h2+self.h1+int((self.img2_canvas_size-self.h2)/2), 
        self.w1+int((self.img2_canvas_size-self.w2)/2):self.w1+self.w2+int((self.img2_canvas_size-self.w2)/2),
        :3] = self.img2
        vis1[:self.h1,:self.w1,:3] = self.img1
        h,w = vis1.shape[:2]

        centrex1 = w/2
        centrey1 = h/2

        x_off = centrex - centrex * r_cos + centrey * r_sin + t_x
        y_off = centrey - centrex * r_sin - centrey * r_cos + t_y

        x_off1 = centrex1 - centrex1 * r_cos1 + centrey1 * r_sin1 + t_x1
        y_off1 = centrey1 - centrex1 * r_sin1 - centrey1 * r_cos1 + t_y1

        M1 = np.float32([[a*r_cos,-b*r_sin, x_off],[c*r_sin,d*r_cos,y_off],[0,0,1]])
        vis1 = cv2.warpPerspective(vis1,M1,(w,h))
        M2 = np.float32([[a1*r_cos1,-b1*r_sin1, x_off1],[c1*r_sin1,d1*r_cos1,y_off1],[0,0,1]])
        vis2 =cv2.warpPerspective(vis2,M2,(w,h))
        added_image = cv2.addWeighted(vis1,1,vis2,1,0)

        cv2.imwrite("output.jpg",added_image)
        cv2.imshow('image',added_image)
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

    def set_canvas(self):
        self.canvas = np.zeros((self.h1*2+self.img2_canvas_size,self.w1*2+self.img2_canvas_size,3), dtype=np.uint8)
        self.canvas[self.h1+int((self.img2_canvas_size-self.h2)/2):self.h2+self.h1+int((self.img2_canvas_size-self.h2)/2), 
        self.w1+int((self.img2_canvas_size-self.w2)/2):self.w1+self.w2+int((self.img2_canvas_size-self.w2)/2),
        :3] = self.img2
        self.canvas[:self.h1,:self.w1,:3] = self.img1
        self.coor_system = CoordinateSystem((len(self.canvas[0])/2,len(self.canvas)/2))

    def run_nelder_mead(self,i,n):
        x0 = []
        for i in range(12):
            param = random.uniform(0,3)
            x0.append(param)
        print("Iteration N: ",i,"/",n+1)
        res = minimize(self.calculateLoss,x0, method = 'nelder-mead', options={'disp':True})
        print("\n\n\n\n")
        return [res.fun,res.x]

    def mosaicImages(self,n):
        print("\n\n\n")
        self.set_canvas()
        h,w = self.canvas.shape[:2]
        savedParameters = [[],[]]
        for i in range(n):
            x0 = []
            for k in range(2):
                for j in range(4):
                    param = random.uniform(0.4,1.8)
                    x0.append(param)
                x0.append(random.uniform(0,360))
                x0.append(random.uniform(0,w-5))
                x0.append(random.uniform(0,h-5))
            print("Iteration N: ",i+1,"/",n+1)
            res = minimize(self.calculateLoss,x0, method = 'nelder-mead', options={'disp':True})
            savedParameters[0].append(res.fun)
            savedParameters[1].append(res.x)
            print("\n\n\n\n")
        minimumErrorIndex = savedParameters[0].index(min(savedParameters[0]))
        print("\n\n\n\n\n\n")
        print(savedParameters)
        print("\n\n\n\n\n\n")
        print("Error Index: ",minimumErrorIndex)
        print("Minimum Loss: ",savedParameters[0][minimumErrorIndex])
        print("Shift_X: ",savedParameters[1][minimumErrorIndex][0]*(self.w1+self.w2))
        print("Shift_Y: ",savedParameters[1][minimumErrorIndex][1]*(self.w1+self.w2))
        print("Thetha: ",savedParameters[1][minimumErrorIndex][2]*360)
        self.BestX = int(savedParameters[1][minimumErrorIndex][0]*(self.w1+self.w2))
        self.BestY = int(savedParameters[1][minimumErrorIndex][1]*(self.h1+self.h2))
        self.Best_Rotate = int(savedParameters[1][minimumErrorIndex][2]*360)
    
    def test_one_iter(self, x0):
        print("\n\n\n")
        self.set_canvas()
        h,w = self.canvas.shape[:2]
        savedParameters = [[],[]]
        print("Iteration N: ",1,"/",1)
        loss = self.calculateLoss(x0)
        print(loss)