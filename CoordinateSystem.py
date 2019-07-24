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
from matplotlib.path import Path

# import sys
import time
SAMPLING_RATE = 5

class CoordinateSystem:
    rectangle1 = []
    rectangle2 = []
    centreOfRectangle2 = None
    polygon1 = None
    polygon2 = None

    def __init__(self,centre):
        self.centreOfRectangle2 = centre
        CAP_STYLE.flat
    
    def set_rectangles(self,rectangles):
        # plt.clf()
        # plt.gca().invert_yaxis()
        self.rectangle1, self.rectangle2 = rectangles
        self.polygon1 = Polygon(self.rectangle1)
        self.polygon2 = Polygon(self.rectangle2)
        # rec1 = Polygon(self.rectangle1)	
        # rec2 = Polygon(self.rectangle2)	
        # x1, y1 =rec1.exterior.xy	
        # x2, y2 =rec2.exterior.xy	
        # plt.plot(x1, y1,color='yellow')
        # plt.plot(x2, y2,color='black')
        
    def rotateElement(self,geometricFigure, thethaInDeg):
        # Start = time.time()
        thetha = thethaInDeg * math.pi/180
        a = math.cos(thetha)
        b = math.sin(thetha)
        centrex, centrey = Polygon(self.rectangle2).centroid.coords.xy
        centrex, centrey = centrex[0], centrey[0]
        x_off = centrex - centrex * a + centrey * b
        y_off = centrey - centrex * b - centrey * a
        M = [a, -b, b, a, x_off, y_off]

        rotated = affine_transform(geometricFigure,M)
        # rotated = rotate(geometricFigure,thethaInDeg,origin=Point(centrex,centrey))
        rotated = loads(dumps(rotated, rounding_precision=0))
        # end = time.time()
        # print("Rotate line: ",end-Start,"\n\n" )
        return rotated
    
    def shiftAnElement(self,geometric_figure, SHIFT_X,SHIFT_Y):
        M = [1,0,0,1,SHIFT_X,SHIFT_Y]
        rotated = affine_transform(geometric_figure,M)
        rotated = loads(dumps(rotated, rounding_precision=0))
        # x,y = rotated.coords.xy
        # plt.plot(x,y,color='magenta')
        return rotated

    def transform(self,M,shape):
        return affine_transform(shape,M)

    def get_intersection_polygon(self):
        # Start = time.time()
        p1 = self.polygon1
        x1,y1= p1.exterior.xy
        p2 = self.polygon2
        p2 = loads(dumps(p2, rounding_precision=0))
        x2,y2= p2.exterior.xy
        intersection = p1.intersection(p2)
        # end = time.time()
        # print("get intersection: ",end-Start ,"\n\n")
        return intersection

    def get_coordinates_in_polygon(self, polygon):
        #Start = time.time()
        p1 = Polygon(self.rectangle1)
        if (polygon.area <= p1.area*0.04):
            return -1
        polygon = loads(dumps(polygon, rounding_precision=0))
        rectangle = list(polygon.exterior.coords)
        bounds = polygon.bounds
        height = int(bounds[3]) - int(bounds[1])
        width = int(bounds[2]) - int(bounds[0])
        p = Path(rectangle)
        x, y = np.meshgrid(np.arange(int(bounds[0]),int(bounds[2])), np.arange(int(bounds[1]),int(bounds[3]))) # make a canvas with coordinates
        x, y = x.flatten(), y.flatten()
        points = np.vstack((x,y)).T

        grid = p.contains_points(points)
        mask = grid.reshape(width,height)
        coords = np.nonzero(np.flip(mask,axis=0))
        coords = np.array(coords)
        coords[0] = coords[0]+int(bounds[0])
        coords[1] = coords[1]+int(bounds[1])
        coordsInTupples = list(tuple(map(tuple, coords.transpose())))
        #end = time.time()
        #print("geting the coornates: ",end-Start,"\n\n" )
        return LineString(coordsInTupples)

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
            self.polygon2 = self.rotateElement(self.polygon2,thetha)
        self.polygon1 = self.shiftAnElement(self.polygon1,SHIFT_X,SHIFT_Y)
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
        initialPolygon2 = self.rotateElement(coordintes_of_intersection,-thetha)
        initialPolygon1 = self.shiftAnElement(coordintes_of_intersection,-SHIFT_X,-SHIFT_Y)
        # x2, y2 =initialPolygon2.coords.xy	
        # plt.plot(x2, y2,color='blue')
        numpy_coords_1 = self.get_numpy_coords(initialPolygon1)
        numpy_coords_2 = self.get_numpy_coords(initialPolygon2)
        coordinates_in_polygon1 = self.make_image_format_indexing(numpy_coords_1)
        coordinates_in_polygon2 = self.make_image_format_indexing(numpy_coords_2)
        coordinates_in_polygon1 = self.makeImageCoordinateFormat(coordinates_in_polygon1)
        coordinates_in_polygon2 = self.makeImageCoordinateFormat(coordinates_in_polygon2)
        # plt.axis('equal')
        # plt.savefig("polygon.png")
        return (coordinates_in_polygon1, coordinates_in_polygon2)