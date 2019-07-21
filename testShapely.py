from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.affinity import affine_transform
from shapely.geometry import LineString
from shapely.wkt import loads
from shapely.wkt import dumps
import matplotlib.pyplot as plt
import numpy as np

polyg = Polygon([(0,0),(0,10.23),(10.12,10.1),(10,0.4)])
print(loads(dumps(polyg, rounding_precision=0)))