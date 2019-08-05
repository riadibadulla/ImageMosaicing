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
        # plt.figure(figsize=(9,9))
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
        # x1,y1= p1.exterior.xy
        p2 = self.polygon2
        # p2 = loads(dumps(p2, rounding_precision=0))
        # x2,y2= p2.exterior.xy
        intersection = p1.intersection(p2)
        # end = time.time()
        # print("get intersection: ",end-Start ,"\n\n")
        return intersection

    def get_coordinates_in_polygon(self, polygon):
        # Start = time.time()
        p1 = self.polygon1
        if (polygon.area <= p1.area*0.02):
            return -1
        polygon = loads(dumps(polygon, rounding_precision=0))
        rectangle = polygon.exterior.coords
        bounds = self.canvas.bounds
        height = int(bounds[3]) - int(bounds[1])
        width = int(bounds[2]) - int(bounds[0])
        p = Path(rectangle)
        x, y = np.meshgrid(np.arange(height), np.arange(width)) # make a canvas with coordinates
        x, y = x.flatten(), y.flatten()
        points = np.vstack((y,x)).T

        grid = p.contains_points(points)
        mask = grid.reshape(width,height)
        coords = np.nonzero(mask)
        coords = np.array(coords)
        # coordsInTupples = list(tuple(map(tuple, coords.transpose())))
        # end = time.time()
        # print("geting the coornates: ",end-Start,"\n\n" )
        return LineString(coords.T)

    def get_numpy_coords(self, shape):
        coordintes = np.array(shape.xy)
        return coordintes

    def make_image_format_indexing(self,coordintes):
        #0.034s
        # Start = time.time()
        new_format = np.repeat(coordintes,3,1)
        new_format = np.append(new_format,np.array([np.tile(np.array([0,1,2]),int(len(coordintes[0])))]),axis=0)
        new_format = np.around(new_format).astype(int)
        # end = time.time()
        # print("Numpy coornates: ",end-Start,"\n\n")
        return new_format
    
    def makeImageCoordinateFormat(self,new_format):
        return (new_format[1],new_format[0],new_format[2])

    def construct_transformation_matrix(self,parameters,polygon):
        # st = time.time()
        s_x,s_y,a,b,thetha_degrees,t_x,t_y = parameters
        thetha = thetha_degrees * math.pi/180
        r_cos = math.cos(thetha)
        r_sin = math.sin(thetha)

        centrex, centrey = polygon.centroid.coords.xy
        centrex, centrey = centrex[0], centrey[0]

        x_rotate = centrex - centrex * r_cos + centrey * r_sin
        y_rotate = centrey - centrex * r_sin - centrey * r_cos
        a11 = s_x*(r_cos-b*r_sin)
        a12 = s_x*(a*r_cos-r_sin)
        a13 = x_rotate*s_x + centrex*(1-s_x) + t_x
        a21 = s_y*(r_sin+b*r_cos)
        a22 = s_y*(a*r_sin+r_cos)
        a23 = y_rotate*s_y + centrey*(1-s_y) + t_y
        
        M = [a11,a12,a21,a22,a13,a23]
        # en= time.time()
        # print("time ",en-st)
        return M

    def squared_distance_between_centres(self):
        centrex1, centrey1 = self.polygon1.centroid.coords.xy
        centrex2, centrey2 = self.polygon2.centroid.coords.xy
        centrex1, centrey1 = centrex1[0], centrey1[0]
        centrex2, centrey2 = centrex2[0], centrey2[0]
        return (centrex1-centrex2)**2+(centrey2-centrey1)**2

    def get_indecies_on_rotate(self, parameters):
        # start = time.time()
        s_x,s_y,a,b,thetha,t_x,t_y, s_x1,s_y1,a1,b1,thetha1,t_x1,t_y1  = parameters
        M1 = self.construct_transformation_matrix((s_x,s_y,a,b,thetha,t_x,t_y),self.polygon1)
        M2 = self.construct_transformation_matrix((s_x1,s_y1,a1,b1,thetha1,t_x1,t_y1),self.polygon2)
        self.polygon1 = self.transform(M1,self.polygon1)
        self.polygon2 = self.transform(M2,self.polygon2)
        sqaured_distance = self.squared_distance_between_centres()
        if (not self.satisfaction_test()):
            return -1
        # x2, y2 =self.polygon2.exterior.xy	
        # plt.plot(x2, y2,color='red')
        # x2, y2 =self.polygon1.exterior.xy	
        # plt.plot(x2, y2,color='grey')
        intersection = self.get_intersection_polygon()
        if (intersection.area < 5.0):
            return -1
        coordintes_of_intersection = self.get_coordinates_in_polygon(intersection)
        # x,y = coordintes_of_intersection.coords.xy
        # plt.plot(x,y,color='green')
        if coordintes_of_intersection == -1:
            return -1
        initialPolygon2 = self.transform(self.get_inverse_matrix(M2),coordintes_of_intersection)
        initialPolygon1 = self.transform(self.get_inverse_matrix(M1),coordintes_of_intersection)
        # x2, y2 =initialPolygon2.coords.xy	
        # plt.plot(x2, y2,color='blue')
        # x2, y2 =initialPolygon1.coords.xy	
        # plt.plot(x2, y2,color='blue')
        numpy_coords_1 = self.get_numpy_coords(initialPolygon1)
        numpy_coords_2 = self.get_numpy_coords(initialPolygon2)
        coordinates_in_polygon1 = self.make_image_format_indexing(numpy_coords_1)
        coordinates_in_polygon2 = self.make_image_format_indexing(numpy_coords_2)
        coordinates_in_polygon1 = self.makeImageCoordinateFormat(coordinates_in_polygon1)
        coordinates_in_polygon2 = self.makeImageCoordinateFormat(coordinates_in_polygon2)
        # plt.axis('equal')
        # plt.legend(['Image1','Image2','Transformed image2','Transformed image1', 'Intersection','Intersection coordinates inverted back'], loc='best')
        # plt.title("Obtaining the coordinates")
        # plt.savefig("polygon.png", dpi=700)
        # end = time.time()
        # print("time: ",start-end)
        return (coordinates_in_polygon1, coordinates_in_polygon2,sqaured_distance)