from shapely.geometry import Polygon
from shapely.geometry import CAP_STYLE
from shapely.geometry import Point
from shapely.affinity import affine_transform
from shapely.affinity import rotate
from shapely.geometry import LineString
from shapely.wkt import loads
from shapely.wkt import dumps
import matplotlib.pyplot as plt
import matplotlib
import math
import numpy as np
from joblib import Parallel, delayed
# import sys
import time
SAMPLING_RATE = 10

class CoordinateSystem:
    rectangle1 = []
    rectangle2 = []
    centreOfRectangle2 = None

    def __init__(self,centre):
        self.centreOfRectangle2 = centre
        CAP_STYLE.flat
    
    def set_rectangles(self,rectangles):
        # plt.clf()
        # plt.gca().invert_yaxis()
        self.rectangle1, self.rectangle2 = rectangles
        rec1 = Polygon(self.rectangle1)	
        rec2 = Polygon(self.rectangle2)	
        # x1, y1 =rec1.exterior.xy	
        # x2, y2 =rec2.exterior.xy	
        # plt.plot(x1, y1,color='yellow')
        # plt.plot(x2, y2,color='black')
        
    def rotateElement(self,geometricFigure, thetha):
        # Start = time.time()
        # a = math.cos(thetha)
        # b = math.sin(thetha)
        centrex, centrey = Polygon(self.rectangle2).centroid.coords.xy
        centrex, centrey = centrex[0], centrey[0]
        coords = np.array(geometricFigure.coords)
        rotated = np.array([self.rotateTranslateCoordinates(tuple(point),centrex,centrey,thetha) for point in coords])
        rotated = rotated.T
        # rotated = rotate(geometricFigure, thetha,origin=(centrex,centrey))
        # rotated = loads(dumps(rotated, rounding_precision=0))
        # end = time.time()
        # print("Rotate line: ",end-Start,"\n\n" )
        return rotated.astype(int)

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
        # Start = time.time()
        newRectangle = []
        for coor in self.rectangle2:
            newCorner = self.rotateTranslateCoordinates(coor,self.centreOfRectangle2[0],self.centreOfRectangle2[1],angle)
            newRectangle.append(newCorner)
        self.rectangle2 = newRectangle
        # end = time.time()
        # print("rotate corners: ",end-Start,"\n\n" )
    
    def shiftAnElement(self,geometric_figure, SHIFT_X,SHIFT_Y):
        M = [1,0,0,1,-SHIFT_X,-SHIFT_Y]
        rotated = affine_transform(geometric_figure,M)
        rotated = loads(dumps(rotated, rounding_precision=0))
        # x,y = rotated.coords.xy
        # plt.plot(x,y,color='magenta')
        return rotated

    def get_intersection_polygon(self):
        # Start = time.time()
        p1 = Polygon(self.rectangle1)
        x1,y1= p1.exterior.xy
        p2 = Polygon(self.rectangle2)
        p2 = loads(dumps(p2, rounding_precision=0))
        x2,y2= p2.exterior.xy
        intersection = p1.intersection(p2)
        # end = time.time()
        # print("get intersection: ",end-Start ,"\n\n")
        return intersection

    def get_coordinates_in_polygon(self, polygon):
        #Start = time.time()
        p1 = Polygon(self.rectangle1)
        if (polygon.area <= p1.area*0.15):
            return -1
        coordinatesInPolygon = []
        bounds = polygon.bounds
        height = int(bounds[3]) - int(bounds[1])
        width = int(bounds[2]) - int(bounds[0])
        y_num_samples = round(height/100*SAMPLING_RATE)
        x_num_samples = round(width/100*SAMPLING_RATE)
        y_step = int(round(height/y_num_samples))
        x_step = int(round(width/x_num_samples))
        if (x_step<1):
            x_step = 1
        if (y_step<1):
            y_step = 1
        bounds = polygon.bounds

        for y in range(int(bounds[1]),int(bounds[3]),int(y_step)):
            for x in range(int(bounds[0]),int(bounds[2]), int(x_step)):
                point = Point(x,y)
                if (point.within(polygon)):
                    coordinatesInPolygon.append(point)
        if (len(coordinatesInPolygon)<=3):
            return -1
        #end = time.time()
        #print("geting the coornates: ",end-Start,"\n\n" )
        return LineString(coordinatesInPolygon)

    def get_numpy_coords(self, shape):
        coordintes = np.array(shape.xy)
        return coordintes

    def make_image_format_indexing(self,coordintes):
        # Start = time.time()
        new_format = np.repeat(coordintes,3,1)
        new_format = np.append(new_format,np.array([np.tile(np.array([0,1,2]),int(len(coordintes[0])))]),axis=0)
        # end = time.time()
        # print("Numpy coornates: ",end-Start,"\n\n")
        new_format = np.around(new_format).astype(int)
        return new_format
    
    def makeImageCoordinateFormat(self,new_format):
        return (new_format[1],new_format[0],new_format[2])

    def get_indecies_on_rotate(self, SHIFT_X, SHIFT_Y, thetha):
        if (thetha != 0):
            self.rotateCornersOfImage2(thetha)
        # x2, y2 =Polygon(self.rectangle2).exterior.xy	
        # plt.plot(x2, y2,color='red')
        intersection = self.get_intersection_polygon()
        if (intersection.area == 0.0):
            return -1
        # x2, y2 =intersection.exterior.xy	
        # plt.plot(x2, y2,color='green')
        coordintes_of_intersection = self.get_coordinates_in_polygon(intersection)
        if coordintes_of_intersection == -1:
            return -1
        numpy_coords_2 = self.rotateElement(coordintes_of_intersection,-thetha)
        initialPolygon1 = self.shiftAnElement(coordintes_of_intersection,SHIFT_X,SHIFT_Y)
        # x2, y2 =initialPolygon2.coords.xy	
        # plt.plot(x2, y2,color='blue')
        numpy_coords_1 = self.get_numpy_coords(initialPolygon1)
        coordinates_in_polygon1 = self.make_image_format_indexing(numpy_coords_1)
        coordinates_in_polygon2 = self.make_image_format_indexing(numpy_coords_2)
        coordinates_in_polygon1 = self.makeImageCoordinateFormat(coordinates_in_polygon1)
        coordinates_in_polygon2 = self.makeImageCoordinateFormat(coordinates_in_polygon2)
        # plt.axis('equal')
        # plt.savefig("polygon.png")
        return (coordinates_in_polygon1, coordinates_in_polygon2)