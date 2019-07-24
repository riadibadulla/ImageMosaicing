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

M = [1, 2, 0, 1, 5, 3]
rotated = affine_transform(polyg,M)
print(rotated)


M_matrix = [[M[0],M[1],M[4]],[M[2],M[3],M[5]],[0,0,1]]
np_matrix = np.matrix(M_matrix)
np_matrix_inverse = np.array(np_matrix.I)
M_inverse = [np_matrix_inverse[0][0],np_matrix_inverse[0][1],np_matrix_inverse[1][0],np_matrix_inverse[1][1],np_matrix_inverse[0][2],np_matrix_inverse[1][2]]
back = affine_transform(rotated,M_inverse)
print(back)

# x1,y1 = rotated.exterior.coords.xy
# plt.plot(x1,y1)
# plt.savefig("poly.png")