from shapely.geometry import Polygon
from shapely.geometry import Point
import math

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
            newCorner = rotateTranslateCoordinates(coor,self.centreOfRectangle2[0],self.centreOfRectangle2[1],angle)
            newRectangle.append(newCorner)
        self.rectangle2 = newRectangle