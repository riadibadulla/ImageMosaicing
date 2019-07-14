import numpy as np
import math
from shapely.geometry import Polygon
from shapely.geometry import Point
import time

def rotateTranslateCoordinates(coor,centreX,centreY,angle):
    X,Y = coor
    tempX = X - centreX
    tempY = Y - centreY
    rotatedX = tempX*math.cos(angle * math.pi/180) - tempY*math.sin(angle * math.pi/180)
    rotatedY = tempX*math.sin(angle * math.pi/180) + tempY*math.cos(angle * math.pi/180)
    x = rotatedX + centreX
    y = rotatedY + centreY
    return x,y


def getCentreOfPolygon(coordinates):
    p = Polygon(coordinates)
    bound = p.bounds
    centreX = (bound[2] + bound[0])/2
    centreY = (bound[3] + bound[1])/2
    return centreX,centreY

def rotateCornersOfImage(rectangle, centre,angle):
    newRectangle = []
    for coor in rectangle:
        newCorner = rotateTranslateCoordinates(coor,centre[0],centre[1],angle)
        newRectangle.append(newCorner)
    return newRectangle

def getCoordinatesInPolygon(intersection):
    bounds = intersection.bounds
    coordinatesInPolygon = []
    for y in range(int(bounds[1]),int(bounds[3])):
        for x in range(int(bounds[0]),int(bounds[2])):
            if (intersection.contains(Point(x,y))):
                coordinatesInPolygon.append((x,y))
    return coordinatesInPolygon

def getCoorOfIntersectionInInitImg(coordinatesInPolygon,centreOfRectangle,angle):
    listOfInitialCoor = []
    for coor in coordinatesInPolygon:
        listOfInitialCoor.append(rotateTranslateCoordinates(coor,centreOfRectangle[0],centreOfRectangle[1],angle))
    return listOfInitialCoor


START_TIME = time.time()

rectangle1 = [(0,0),(0,10),(10,10),(10,0)]
rectangle2 = [(10,0),(10,10),(20,10),(20,0)]
centreOfRectangle1 = getCentreOfPolygon(rectangle1)
centreOfRectangle2 = getCentreOfPolygon(rectangle2)
rectangle1 = rotateCornersOfImage(rectangle1,centreOfRectangle1,45)
rectangle2 = rotateCornersOfImage(rectangle2,centreOfRectangle2,45)

p1 = Polygon(rectangle1)
p2 = Polygon(rectangle2)
intersection = p1.intersection(p2)
coordinatesInPolygon = getCoordinatesInPolygon(intersection)
initialCoord1 = getCoorOfIntersectionInInitImg(coordinatesInPolygon,centreOfRectangle1,-45)
print(initialCoord1)

END_Time = time.time()
print(END_Time-START_TIME)

