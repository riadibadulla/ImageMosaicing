from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.affinity import affine_transform
from shapely.geometry import LineString
import matplotlib.pyplot as plt
import numpy as np

polyg = Polygon([(0,0),(0,10),(10,10),(10,0)])
int_coords = lambda x: np.array(x).round().astype(np.int32)
interiors = [int_coords(pi.coords) for poly in [polyg]
                 for pi in poly.interiors]
print(interiors)