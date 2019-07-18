from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.affinity import affine_transform
from shapely.geometry import LineString
import matplotlib.pyplot as plt
import math
import numpy as np
import sys
import time

class CoordinateSystem:
    rectangle1 = []
    rectangle2 = []
    centreOfRectangle2 = None

    def __init__(self,centre):
        self.centreOfRectangle2 = centre
    
    def set_rectangles(self,rectangles):
        self.rectangle1, self.rectangle2 = rectangles

    def rotateElement(self,geometricFigure, thetha):
        # Start = time.time()
        a = math.cos(thetha)
        b = math.sin(thetha)
        centrex = self.centreOfRectangle2[0]
        centrey = self.centreOfRectangle2[1]
        #M = [[a,b,(1-a)*centrex*centrey],[-b,a,b*centrex+(1-a)*centrey],[0,0,1]]
        M = [a,b,-b,a,(1-a)*centrex-b*centrey,b*centrex+(1-a)*centrey]
        rotated = affine_transform(geometricFigure,M)
        # end = time.time()
        # print("Rotate line: ",end-Start,"\n\n" )
        return rotated

    def rotateTranslateCoordinates(self,coor,centreX,centreY,angle):
        X,Y = coor
        tempX = X - centreX
        tempY = Y - centreY
        rotatedX = tempX*math.cos(angle * math.pi/180) - tempY*math.sin(angle * math.pi/180)
        rotatedY = tempX*math.sin(angle * math.pi/180) + tempY*math.cos(angle * math.pi/180)
        x = rotatedX + centreX
        y = rotatedY + centreY
        return x,y

    def rotateCornersOfImage2(self,angle):
        p2 = Polygon(self.rectangle2)
        x, y =p2.exterior.xy
        plt.plot(x, y, color='blue', alpha=0.7,linewidth=3, solid_capstyle='round', zorder=2)
        # Start = time.time()
        newRectangle = []
        for coor in self.rectangle2:
            newCorner = self.rotateTranslateCoordinates(coor,self.centreOfRectangle2[0],self.centreOfRectangle2[1],angle)
            newRectangle.append(newCorner)
        self.rectangle2 = newRectangle
        # end = time.time()
        # print("rotate corners: ",end-Start,"\n\n" )
    
    def get_intersection_polygon(self):
        # Start = time.time()
        p1 = Polygon(self.rectangle1)
        x1,y1= p1.exterior.xy
        p2 = Polygon(self.rectangle2)
        x2,y2= p2.exterior.xy
        intersection = p1.intersection(p2)
        # end = time.time()
        # print("get intersection: ",end-Start ,"\n\n")
        x,y = intersection.exterior.xy
        plt.plot(x1, y1, color='red', alpha=0.7,linewidth=3, solid_capstyle='round', zorder=2)
        # plt.plot(x2, y2, color='blue', alpha=0.7,linewidth=3, solid_capstyle='round', zorder=2)
        plt.plot(x, y, color='yellow', alpha=0.7,linewidth=3, solid_capstyle='round', zorder=2)
        # plt.set_title('Polygon')
        return intersection

    def get_coordinates_in_polygon(self, polygon):
        # Start = time.time()
        if (polygon.area == 0.0):
            return []
        coordinatesInPolygon = []
        bounds = polygon.bounds
        for y in range(int(bounds[1]),int(bounds[3])):
            for x in range(int(bounds[0]),int(bounds[2])):
                point = Point(x,y)
                if (point.within(polygon)):
                    coordinatesInPolygon.append(point)
        if (len(coordinatesInPolygon)<=3):
            return -1
        # end = time.time()
        # print("geting the coornates: ",end-Start,"\n\n" )
        return LineString(coordinatesInPolygon)

    def make_image_format_indexing(self,coordintes):
        # Start = time.time()
        coordintes = np.array(coordintes.xy)
        new_format = np.repeat(coordintes,3,1)
        new_format = np.append(new_format,np.array([np.tile(np.array([0,1,2]),int(len(coordintes[0])))]),axis=0)
        # end = time.time()
        # print("Numpy coornates: ",end-Start,"\n\n")
        return new_format.astype(int)
    
    def get_indecies_on_rotate(self, SHIFT_X, SHIFT_Y, thetha):
        if (thetha != 0):
            self.rotateCornersOfImage2(thetha)
        intersection = self.get_intersection_polygon()
        if (intersection.area == 0.0):
            return -1
        
        coordintes_of_intersection = self.get_coordinates_in_polygon(intersection)
        if coordintes_of_intersection == -1:
            return -1
        initialPolygon2 = self.rotateElement(coordintes_of_intersection,360-thetha)
        x,y = initialPolygon2.coords.xy
        plt.plot(x, y, color='black', alpha=0.7,linewidth=3, solid_capstyle='round', zorder=2)
        plt.show()
        coordinates_in_polygon1 = self.make_image_format_indexing(coordintes_of_intersection)
        coordinates_in_polygon2 = self.make_image_format_indexing(initialPolygon2)
        coordinates_in_polygon1[0] = coordinates_in_polygon1[0] - SHIFT_X
        coordinates_in_polygon1[1] = coordinates_in_polygon1[1] - SHIFT_Y

        return (coordinates_in_polygon1, coordinates_in_polygon2)