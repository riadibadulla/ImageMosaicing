import cv2
import numpy as np
import time 
from scipy.optimize import minimize
from scipy.optimize import brute
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
    best_loss = None
    best_parameters = [-0.25,-0.25,0,0,0,0,0,-0.25,-0.25,0,0,0,0,0]

    max_possible_error = 0

    def __init__(self, img1, img2, resize):
        self.img1 = img1
        self.img2 = img2
        if (resize):
            self.img1 = cv2.resize(self.img1,None,fx=0.4,fy=0.4)
            self.img2 = cv2.resize(self.img2,None,fx=0.4,fy=0.4)
        self.h1, self.w1 = self.img1.shape[:2]
        self.h2, self.w2 = self.img2.shape[:2]
        self.img2_canvas_size = int(math.sqrt(math.pow(self.h2,2)+math.pow(self.w2,2)))
        self.max_possible_error = 255*3*self.w1*self.h1*self.h2*self.w2*100
        self.best_loss = self.max_possible_error
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
        s_x,s_x1 = (s_x+0.75)/0.5, (s_x1+0.75)/0.5
        s_y,s_y1 = (s_y+0.75)/0.5, (s_y1+0.75)/0.5
        a,a1 = a*0.3/0.5, a1*0.3/0.5
        b,b1 = b*0.3/0.5 ,b1*0.3/0.5
        thetha, thetha1 = thetha*360/0.5, thetha1*360/0.5
        h,w = self.canvas.shape[:2]
        t_x, t_x1 = t_x*w/2/0.5, t_x1*w/2/0.5
        t_y, t_y1 = t_y*h/2/0.5, t_y1*h/2/0.5
        return [s_x,s_y,a,b,thetha,t_x,t_y, s_x1,s_y1,a1,b1,thetha1,t_x1,t_y1]

    def regularise(self,parameters, distance):
        scale_alpha = 0.001
        shear_aplha = 0.001
        distance_alpha = 0.005
        regularisation = (math.pow(parameters[2],2)+math.pow(parameters[3],2)+math.pow(parameters[9],2)+math.pow(parameters[10],2))*shear_aplha
        + distance*distance_alpha
        + (math.pow(parameters[0],2)+math.pow(parameters[1],2)+math.pow(parameters[7],2)+math.pow(parameters[8],2))*scale_alpha
        return regularisation


    def calculateLoss(self,parameters):
        #sys.stdout.write("\r Parameters:{0}      ☚||||".format(parameters[:]))
        parameters = self.unnormalise(parameters)
        self.coor_system.set_rectangles(self.getCornersOfImages())
        coordinates_of_intersection = self.coor_system.get_indecies_on_rotate(parameters)
        if (coordinates_of_intersection == -1):
            return self.max_possible_error
        difference = np.square(np.subtract(self.canvas[coordinates_of_intersection[0]],self.canvas[coordinates_of_intersection[1]]))
        loss = np.mean(difference)
        regularisation = self.regularise(coordinates_of_intersection[2])
        loss = loss + regularisation
        sys.stdout.write("\r  Loss:{0} , Regularisation:{1} ☚||||".format(loss,parameters, regularisation))
        # print(loss)
            # + *10
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
        # vis1_without2 = cv2.subtract(vis1,vis2)
        added_image = cv2.addWeighted(vis1,1,vis2,1,0)

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

    def clear_previous_iteration(self):
        for j in range(4):
            sys.stdout.write("\033[F")
        for j in range(4):
            print("                                                                                           ")
        for j in range(4):
            sys.stdout.write("\033[F") 
    
    def optimese_translations(self, passed_values):
        t_x, t_y, t_x1,t_y1 = passed_values
        parameters = self.best_parameters.copy()
        parameters[5], parameters[6] = t_x, t_y
        parameters[12], parameters[13] = t_x1, t_y1
        return self.calculateLoss(parameters)
    
    def optimese_rotation(self, passed_values):
        thetha, thetha1 = passed_values
        parameters = self.best_parameters.copy()
        parameters[4], parameters[11] = thetha, thetha1
        return self.calculateLoss(parameters)
        
    def optimese_scale(self, passed_values):
        s_x, s_y, s_x1, s_y1 = passed_values
        parameters = self.best_parameters.copy()
        parameters[0], parameters[1] = s_x, s_y
        parameters[7], parameters[8] = s_x1, s_y1
        return self.calculateLoss(parameters)
    
    def optimese_shear(self,passed_values):
        a, b, a1, b1 = passed_values
        parameters = self.best_parameters.copy()
        parameters[2], parameters[3] = a, b
        parameters[9], parameters[10] = a1, b1
        return self.calculateLoss(parameters)

    def mosaicImages(self,n):
        print("\n\n\n")
        self.set_canvas()
        h,w = self.canvas.shape[:2]
        i=0
        while (i<n):
            print("Iteration N: ",i+1,"/",n)
            start = time.time()
            for k in range(100):
                t = [random.uniform(0,0.5) for j in range(4)]
                res = minimize(self.optimese_translations,t, method = 'nelder-mead', options={'disp':True, 'adaptive':True, 'fatol':10})
                if (res.fun == self.max_possible_error):
                    self.clear_previous_iteration()
                    continue
                if (self.best_loss>res.fun):
                    self.best_loss = res.fun
                    self.best_parameters[5], self.best_parameters[6] = res.x[0], res.x[1]
                    self.best_parameters[12], self.best_parameters[13] = res.x[2], res.x[3]
                break
            for k in range(100):
                r = [random.uniform(0,0.5) for j in range(2)]
                res = minimize(self.optimese_rotation,r, method = 'nelder-mead', options={'disp':True, 'adaptive':True, 'fatol':10})
                if (res.fun == self.max_possible_error):
                    self.clear_previous_iteration()
                    continue
                if (self.best_loss>res.fun):
                    self.best_loss = res.fun
                    self.best_parameters[4], self.best_parameters[11] = res.x[0], res.x[1]
                break
            for k in range(100):
                s = [random.uniform(0,0.5) for j in range(4)]
                res = minimize(self.optimese_scale,s, method = 'nelder-mead', options={'disp':True, 'adaptive':True, 'fatol':10})
                if (res.fun == self.max_possible_error):
                    self.clear_previous_iteration()
                    continue
                if (self.best_loss>res.fun):
                    self.best_loss = res.fun
                    self.best_parameters[0], self.best_parameters[1] = res.x[0], res.x[1]
                    self.best_parameters[7], self.best_parameters[8] = res.x[2], res.x[3]
                break
            for k in range(100):
                sh = [random.uniform(0,0.5) for j in range(4)]
                res = minimize(self.optimese_shear,sh, method = 'nelder-mead', options={'disp':True, 'adaptive':True, 'fatol':10})
                if (res.fun == self.max_possible_error):
                    self.clear_previous_iteration()
                    continue
                if (self.best_loss>res.fun):
                    self.best_loss = res.fun
                    self.best_parameters[2], self.best_parameters[3] = res.x[0], res.x[1]
                    self.best_parameters[9], self.best_parameters[10] = res.x[2], res.x[3]
                break
            i+=1
            end = time.time()
            print("Time taken: ",end-start)
            print("\n\n\n\n")
        print("\n\n\n\n\n\n")
        print("Minimum Loss: ",self.best_loss)
        print("Parameters ",self.best_parameters)
    
    def test_one_iter(self, x0):
        print("\n\n\n")
        self.set_canvas()
        h,w = self.canvas.shape[:2]
        savedParameters = [[],[]]
        print("Iteration N: ",1,"/",1)
        loss = self.calculateLoss(x0)
        print(loss)