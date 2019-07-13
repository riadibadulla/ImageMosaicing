from shapely.geometry import Polygon
from shapely.geometry import Point
import math
import numpy as np

class CoordinateSystem:
    rectangle1 = []
    rectangle2 = []
    centreOfRectangle2 = None

    def __init__(self, rectangles):
        self.rectangle1, self.rectangle2 = rectangles
        self.centreOfRectangle2 = self.getCentreOfRectangle(self.rectangle2)

    def getCentreOfRectangle(self,coordinates):
        p = Polygon(coordinates)
        bound = p.bounds
        centreX = (bound[2] + bound[0])/2
        centreY = (bound[3] + bound[1])/2
        return centreX,centreY
    
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
        for coor in self.rectangle1:
            newCorner = self.rotateTranslateCoordinates(coor,self.centreOfRectangle2[0],self.centreOfRectangle2[1],angle)
            newRectangle.append(newCorner)
        self.rectangle2 = newRectangle
    
    def get_intersection_polygon(self):
        p1 = Polygon(self.rectangle1)
        p2 = Polygon(self.rectangle2)
        intersection = p1.intersection(p2)
        return intersection

    def get_coordinates_of_intersection(self):
        intersection = self.get_intersection_polygon()
        coordinatesInPolygon = []
        bounds = intersection.bounds
        for y in range(int(bounds[1]),int(bounds[3])):
            for x in range(int(bounds[0]),int(bounds[2])):
                if (intersection.contains(Point(x,y))):
                    coordinatesInPolygon.append((x,y))
        return coordinatesInPolygon
        
    def getCoorOfIntersectionInInitImg2(self,coordinatesInPolygon,centreOfRectangle,angle):
        listOfInitialCoor = []
        for coor in coordinatesInPolygon:
            new_coordinate = self.rotateTranslateCoordinates(coor,centreOfRectangle[0],centreOfRectangle[1],angle)
            new_coordinate = (int(new_coordinate[0]),int(new_coordinate[1]))
            listOfInitialCoor.append(new_coordinate)
        return listOfInitialCoor

    def get_initial_coord1(self,coor_with_shift, SHIFTX, SHIFTY):
        coor = []
        for coor_tupple in coor_with_shift:
            coor.append((int(coor_tupple[0])-SHIFTX,int(coor_tupple[1])-SHIFTY))
        return coor

    def get_numpy_format(self,initialCoordinates):
        values = [[],[],[]]
        for initial_coor in initialCoordinates:
            for i in range(3):
                values[0].append(initial_coor[0])
                values[1].append(initial_coor[1])
                values[2].append(i)
        values = np.array(values)
        return values

    def get_indecies_on_rotate(self, SHIFT_X, SHIFT_Y, thetha):
        self.rotateCornersOfImage2(thetha)
        coordintes_of_intersection = self.get_coordinates_of_intersection()
        initialCoord2 = self.getCoorOfIntersectionInInitImg2(coordintes_of_intersection,self.centreOfRectangle2,-1*thetha)
        initialCoord1 = self.get_initial_coord1(coordintes_of_intersection, SHIFT_X, SHIFT_Y)
        return (self.get_numpy_format(initialCoord1),self.get_numpy_format(initialCoord2))
