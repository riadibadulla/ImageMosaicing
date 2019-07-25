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
    canvas = None

    def __init__(self,centre):
        self.centreOfRectangle2 = centre
        CAP_STYLE.flat
    
    def set_canvas(self,size):
        h,w = size
        corners = [(0,0),(w-5,0),(w-5,h-5),(0,h-5)]
        self.canvas = Polygon(corners)

    def set_rectangles(self,rectangles):
        plt.clf()
        plt.gca().invert_yaxis()
        self.rectangle1, self.rectangle2 = rectangles
        self.polygon1 = Polygon(self.rectangle1)
        self.polygon2 = Polygon(self.rectangle2)
        rec1 = Polygon(self.rectangle1)	
        rec2 = Polygon(self.rectangle2)	
        x1, y1 =rec1.exterior.xy	
        x2, y2 =rec2.exterior.xy	
        plt.plot(x1, y1,color='yellow')
        plt.plot(x2, y2,color='black')
        
    def satisfaction_test(self):
        return (self.polygon1.within(self.canvas) and self.polygon2.within(self.canvas))
    
    def get_inverse_matrix(self,M):
        M_matrix = [[M[0],M[1],M[4]],[M[2],M[3],M[5]],[0,0,1]]
        np_matrix = np.matrix(M_matrix)
        np_matrix_inverse = np.array(np_matrix.I)
        M_inverse = [np_matrix_inverse[0][0],np_matrix_inverse[0][1],np_matrix_inverse[1][0],np_matrix_inverse[1][1],np_matrix_inverse[0][2],np_matrix_inverse[1][2]]
        return M_inverse

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
        # if (polygon.area <= p1.area*0.04):
        #     return -1
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

    def construct_transformation_matrix(self,parameters,polygon):
        a,b,c,d,thetha_degrees,t_x,t_y = parameters
        thetha = thetha_degrees * math.pi/180
        r_cos = math.cos(thetha)
        r_sin = math.sin(thetha)

        centrex, centrey = polygon.centroid.coords.xy
        centrex, centrey = centrex[0], centrey[0]

        x_off = centrex - centrex * r_cos + centrey * r_sin + t_x
        y_off = centrey - centrex * r_sin - centrey * r_cos + t_y
        M = [a*r_cos, -b*r_sin, c*r_sin, d*r_cos, x_off, y_off]
        return M

    def get_indecies_on_rotate(self, parameters):
        a,b,c,d,thetha,t_x,t_y, a1,b1,c1,d1,thetha1,t_x1,t_y1  = parameters
        M1 = self.construct_transformation_matrix((a,b,c,d,thetha,t_x,t_y),self.polygon1)
        M2 = self.construct_transformation_matrix((a1,b1,c1,d1,thetha1,t_x1,t_y1),self.polygon2)
        self.polygon1 = self.transform(M1,self.polygon1)
        self.polygon2 = self.transform(M2,self.polygon2)
        # if (not self.satisfaction_test()):
        #     plt.axis('equal')
        #     plt.savefig("polygon.png")
        #     return -1
        x2, y2 =self.polygon2.exterior.xy	
        plt.plot(x2, y2,color='red')
        x2, y2 =self.polygon1.exterior.xy	
        plt.plot(x2, y2,color='grey')
        intersection = self.get_intersection_polygon()
        if (intersection.area == 0.0):
            plt.axis('equal')
            plt.savefig("polygon.png")
            return -1
        x2, y2 =intersection.exterior.xy	
        plt.plot(x2, y2,color='green')
        coordintes_of_intersection = self.get_coordinates_in_polygon(intersection)
        x,y = coordintes_of_intersection.coords.xy
        plt.plot(x,y,color='green')
        if coordintes_of_intersection == -1:
            plt.axis('equal')
            plt.savefig("polygon.png")
            return -1
        initialPolygon2 = self.transform(self.get_inverse_matrix(M2),coordintes_of_intersection)
        initialPolygon1 = self.transform(self.get_inverse_matrix(M1),coordintes_of_intersection)
        x2, y2 =initialPolygon2.coords.xy	
        plt.plot(x2, y2,color='blue')
        x2, y2 =initialPolygon1.coords.xy	
        plt.plot(x2, y2,color='blue')
        numpy_coords_1 = self.get_numpy_coords(initialPolygon1)
        numpy_coords_2 = self.get_numpy_coords(initialPolygon2)
        coordinates_in_polygon1 = self.make_image_format_indexing(numpy_coords_1)
        coordinates_in_polygon2 = self.make_image_format_indexing(numpy_coords_2)
        coordinates_in_polygon1 = self.makeImageCoordinateFormat(coordinates_in_polygon1)
        coordinates_in_polygon2 = self.makeImageCoordinateFormat(coordinates_in_polygon2)
        plt.axis('equal')
        plt.savefig("polygon.png")
        return (coordinates_in_polygon1, coordinates_in_polygon2)