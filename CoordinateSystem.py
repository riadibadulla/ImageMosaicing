from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.affinity import affine_transform
from shapely.geometry import LineString
import math
import numpy as np
import sys
class CoordinateSystem:
    rectangle1 = []
    rectangle2 = []
    centreOfRectangle2 = None

    def __init__(self,centre):
        self.centreOfRectangle2 = centre
    
    def set_rectangles(self,rectangles):
        self.rectangle1, self.rectangle2 = rectangles

    def rotateElement(self,geometricFigure, thetha):
        a = math.cos(thetha)
        b = math.sin(thetha)
        centrex = self.centreOfRectangle2[0]
        centrey = self.centreOfRectangle2[1]
        #M = [[a,b,(1-a)*centrex*centrey],[-b,a,b*centrex+(1-a)*centrey],[0,0,1]]
        M = [a,b,-b,a,(1-a)*centrex*centrey,b*centrex+(1-a)*centrey]
        return affine_transform(geometricFigure,M)

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
        newRectangle = []
        for coor in self.rectangle2:
            newCorner = self.rotateTranslateCoordinates(coor,self.centreOfRectangle2[0],self.centreOfRectangle2[1],angle)
            newRectangle.append(newCorner)
        self.rectangle2 = newRectangle
    
    def get_intersection_polygon(self):
        p1 = Polygon(self.rectangle1)
        p2 = Polygon(self.rectangle2)
        try:
            intersection = p1.intersection(p2)
        except:
            print("PORCO")
        return intersection

    def get_coordinates_in_polygon(self, polygon):
        if (polygon.area == 0.0):
            return []
        coordinatesInPolygon = []
        bounds = polygon.bounds
        for y in range(int(bounds[1]),int(bounds[3]-1)):
            for x in range(int(bounds[0]),int(bounds[2]-1)):
                if (polygon.contains(Point(x,y))):
                    coordinatesInPolygon.append((x,y))
        return np.array(LineString(coordinatesInPolygon).xy)
        
    # def getCoorOfIntersectionInInitImg2(self,coordinatesInPolygon,centreOfRectangle,angle):
    #     listOfInitialCoor = []
    #     for coor in coordinatesInPolygon:
    #         new_coordinate = self.rotateTranslateCoordinates(coor,centreOfRectangle[0],centreOfRectangle[1],angle)
    #         new_coordinate = (int(new_coordinate[0]),int(new_coordinate[1]))
    #         listOfInitialCoor.append(new_coordinate)
    #     return listOfInitialCoor

    # def get_initial_coord1(self,coor_with_shift, SHIFTX, SHIFTY):
    #     coor = []
    #     for coor_tupple in coor_with_shift:
    #         coor.append((int(coor_tupple[0])-SHIFTX,int(coor_tupple[1])-SHIFTY))
    #     return coor

    # def get_numpy_format(self,initialCoordinates):
    #     values = [[],[],[]]
    #     for initial_coor in initialCoordinates:
    #         for i in range(3):
    #             values[0].append(initial_coor[0])
    #             values[1].append(initial_coor[1])
    #             values[2].append(i)
    #     values = np.array(values)
    #     return values

    def make_image_format_indexing(self,coordintes):
        new_format = np.repeat(coordintes,3,1)
        new_format = np.append(new_format,np.array([np.tile(np.array([0,1,2]),int(len(coordintes[0])))]),axis=0)
        return new_format.astype(int)
    
    def get_indecies_on_rotate(self, SHIFT_X, SHIFT_Y, thetha):
        if (thetha != 0):
            self.rotateCornersOfImage2(thetha)
        intersection = self.get_intersection_polygon()
        if (intersection.area == 0.0):
            return -1
        initialPolygon2 = self.rotateElement(intersection,-1*thetha)
        coordinates_in_polygon1 = self.get_coordinates_in_polygon(intersection)
        coordinates_in_polygon1 = self.make_image_format_indexing(coordinates_in_polygon1)
        coordinates_in_polygon2 = self.get_coordinates_in_polygon(initialPolygon2)
        coordinates_in_polygon2 = self.make_image_format_indexing(coordinates_in_polygon2)
        
        return (coordinates_in_polygon1, coordinates_in_polygon2)
