from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.affinity import affine_transform
from shapely.geometry import LineString
from shapely.wkt import loads
from shapely.wkt import dumps
from shapely.geometry import CAP_STYLE
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
from matplotlib.path import Path
rec = [(10,10),(25,10),(25,25)]

start = time.time()
polyg = Polygon(rec)
bounds = polyg.bounds

rectangle = list(polyg.exterior.coords)

height = int(bounds[3]) - int(bounds[1])
width = int(bounds[2]) - int(bounds[0])
p = Path(rectangle)

x, y = np.meshgrid(np.arange(int(bounds[0]),int(bounds[2])), np.arange(int(bounds[1]),int(bounds[3]))) # make a canvas with coordinates
x, y = x.flatten(), y.flatten()
points = np.vstack((x,y)).T 

grid = p.contains_points(points)
mask = grid.reshape(width,height)
coords = np.nonzero(mask)
coords = np.array(coords)
end = time.time()

coords[0] = coords[0]+int(bounds[0])
coords[1] = coords[1]+int(bounds[1])
coordsInTupples = list(tuple(map(tuple, coords.transpose())))
print(coordsInTupples)
b = LineString(coordsInTupples)
print(end-start)
# x,y = polyg.exterior.coords.xy
# plt.plot(x,y)
# M = [1, 2, 0, 1, 0, 0]
# rotated = affine_transform(polyg,M)
# x1,y1 = rotated.exterior.coords.xy
# plt.plot(x1,y1)
# plt.savefig("poly.png")