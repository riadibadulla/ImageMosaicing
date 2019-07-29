import cv2
import numpy as np
import time 
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
    canvas = None
    coor_system = None
    best_parameters = []

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

    def unnormalise(self, parameters):
        s_x,s_y,a,b,thetha,t_x,t_y, s_x1,s_y1,a1,b1,thetha1,t_x1,t_y1 = parameters
        s_x,s_x1 = (s_x *1.1 +0.65)/0.5, (s_x1 *1.1 +0.65)/0.5
        s_y,s_y1 = (s_y *1.1 +0.65)/0.5, (s_y1 *1.1 +0.65)/0.5
        a,a1 = a*0.3/0.5, a1*0.3/0.5
        b,b1 = b*0.3/0.5 ,b1*0.3/0.5
        thetha, thetha1 = thetha*360/0.5, thetha1*360/0.5
        h,w = self.canvas.shape[:2]
        t_x, t_x1 = t_x*w/2/0.5, t_x1*w/2/0.5
        t_y, t_y1 = t_y*h/2/0.5, t_y1*h/2/0.5
        return [s_x,s_y,a,b,thetha,t_x,t_y, s_x1,s_y1,a1,b1,thetha1,t_x1,t_y1]

    def calculateLoss(self,parameters):
        #sys.stdout.write("\r Parameters:{0}      ☚||||".format(parameters[:]))
        parameters = self.unnormalise(parameters)
        self.coor_system.set_rectangles(self.getCornersOfImages())
        coordinates_of_intersection = self.coor_system.get_indecies_on_rotate(parameters)
        if (coordinates_of_intersection == -1):
            return 255*3*self.w1*self.h1*self.h2*self.w2
        difference = np.square(np.subtract(self.canvas[coordinates_of_intersection[0]],self.canvas[coordinates_of_intersection[1]]))
        loss = np.mean(difference)
        # sys.stdout.write("\r  Loss:{0}       ☚||||".format(loss))
        print(loss)
            # + (parameters[2]+parameters[3]+parameters[9]+parameters[10])*10
        return loss

    def drawImage(self,param,time):
        param = self.unnormalise(param)
        s_x,s_y,a,b,thetha,t_x,t_y, s_x1,s_y1,a1,b1,thetha1,t_x1,t_y1 = param
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

        x_rotate = centrex - centrex * r_cos + centrey * r_sin
        y_rotate = centrey - centrex * r_sin - centrey * r_cos

        x_rotate1 = centrex1 - centrex1 * r_cos1 + centrey1 * r_sin1
        y_rotate1 = centrey1 - centrex1 * r_sin1 - centrey1 * r_cos1

        a11 = s_x*(r_cos-b*r_sin)
        a12 = s_x*(a*r_cos-r_sin)
        a13 = x_rotate*s_x + centrex*(1-s_x) + t_x
        a21 = s_y*(r_sin+b*r_cos)
        a22 = s_y*(a*r_sin+r_cos)
        a23 = y_rotate*s_y + centrey*(1-s_y) + t_y

        M1 = np.float32([[a11,a12, a13],[a21,a22,a23],[0,0,1]])
        vis1 = cv2.warpPerspective(vis1,M1,(w,h))

        a11 = s_x1*(r_cos1-b1*r_sin1)
        a12 = s_x1*(a1*r_cos1-r_sin1)
        a13 = x_rotate1*s_x1 + centrex1*(1-s_x1) + t_x1
        a21 = s_y1*(r_sin1+b1*r_cos1)
        a22 = s_y1*(a1*r_sin1+r_cos1)
        a23 = y_rotate1*s_y1 + centrey1*(1-s_y1) + t_y1

        M2 = np.float32([[a11,a12, a13],[a21,a22,a23],[0,0,1]])        
        vis2 =cv2.warpPerspective(vis2,M2,(w,h))
        vis1_without2 = cv2.subtract(vis1,vis2)
        added_image = cv2.addWeighted(vis1_without2,1,vis2,1,0)

        cv2.imwrite("output.jpg",added_image)
        cv2.imshow('image',added_image)
        cv2.waitKey(time)

    def set_canvas(self):
        self.canvas = np.zeros((self.h1*2+self.img2_canvas_size,self.w1*2+self.img2_canvas_size,3), dtype=np.uint8)
        self.canvas[self.h1+int((self.img2_canvas_size-self.h2)/2):self.h2+self.h1+int((self.img2_canvas_size-self.h2)/2), 
        self.w1+int((self.img2_canvas_size-self.w2)/2):self.w1+self.w2+int((self.img2_canvas_size-self.w2)/2),
        :3] = self.img2
        self.canvas[:self.h1,:self.w1,:3] = self.img1
        self.coor_system = CoordinateSystem((len(self.canvas[0])/2,len(self.canvas)/2))
        self.coor_system.set_canvas(self.canvas.shape[:2])

    def clear_previousPiteration(self):
        for j in range(5):
            sys.stdout.write("\033[F")
        for j in range(5):
            print("                                                                                           ")
        for j in range(5):
            sys.stdout.write("\033[F") 

    def mosaicImages(self,n):
        print("\n\n\n")
        self.set_canvas()
        h,w = self.canvas.shape[:2]
        savedParameters = [[],[]]
        i=0
        while (i<n):
            x0 = [random.uniform(0,0.5) for j in range(14)]
            print("Iteration N: ",i+1,"/",n)
            start = time.time()
            res = minimize(self.calculateLoss,x0, method = 'nelder-mead', options={'disp':True, 'adaptive':True})
            # res = minimize(self.calculateLoss,x0, method = 'COBYLA', options={'disp':True})
            if (res.fun == 255*3*self.w1*self.h1*self.h2*self.w2):
                # self.clear_previousPiteration()
                continue
            savedParameters[0].append(res.fun)
            savedParameters[1].append(res.x)
            i+=1
            end = time.time()
            print("Time taken: ",end-start)
            print("\n\n\n\n")
        minimumErrorIndex = savedParameters[0].index(min(savedParameters[0]))
        print("\n\n\n\n\n\n")
        print(savedParameters)
        print("\n\n\n\n\n\n")
        print("Error Index: ",minimumErrorIndex)
        print("Minimum Loss: ",savedParameters[0][minimumErrorIndex])
        print("Parameters ",savedParameters[1][minimumErrorIndex])
        self.best_parameters = savedParameters[1][minimumErrorIndex]
    
    def test_one_iter(self, x0):
        print("\n\n\n")
        self.set_canvas()
        h,w = self.canvas.shape[:2]
        savedParameters = [[],[]]
        print("Iteration N: ",1,"/",1)
        loss = self.calculateLoss(x0)
        print(loss)