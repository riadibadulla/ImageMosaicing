from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.affinity import affine_transform
from shapely.geometry import LineString
from shapely.wkt import loads
from shapely.wkt import dumps
from shapely.geometry import CAP_STYLE
import matplotlib.pyplot as plt
import numpy as np

# polyg = Polygon([(0,0),(0,10.23),(10.12,10.1),(10,0.4)])
# # print(loads(dumps(polyg, rounding_precision=0)))
# a = polyg.buffer(0.01,cap_style=CAP_STYLE.round)
# print(a)

b = Point(1, 1).buffer(1.5, resolution=2)
print(b)
