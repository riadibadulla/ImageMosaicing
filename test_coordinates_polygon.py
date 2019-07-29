from shapely.geometry import Polygon
import time
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
from matplotlib.path import Path
from shapely.geometry import asLineString

canvas = Polygon([(0,0),(0,300),(300,300),(0,300)])

def get_coordinates_in_polygon(polygon):
    Start = time.time()
    polygon = loads(dumps(polygon, rounding_precision=0))
    rectangle = polygon.exterior.coords
    bounds = canvas.bounds
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
    end = time.time()
    print("geting the coornates: ",end-Start,"\n\n" )
    return asLineString(coords.T)


rec = [(50,50),(100,70),(100,110),(40,80)]
polygon = Polygon(rec)
coord = get_coordinates_in_polygon(polygon)
x,y = coord.coords.xy
plt.plot(x,y)
plt.show()
plt.savefig("yes.png")