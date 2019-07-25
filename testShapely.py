from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.affinity import affine_transform
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
import math
from matplotlib.path import Path

rec = [(10,10),(25,10),(25,25),(10,25)]

canvas= [(0,0),(24,0),(24,100),(0,100)]

start = time.time()
polyg = Polygon(rec)
can_polygon = Polygon(canvas)
print(polyg.within(can_polygon))




# x,y = polyg.exterior.coords.xy
# centrex, centrey = polyg.centroid.coords.xy
# centrex, centrey = centrex[0], centrey[0]
# plt.plot(x,y, color='red')

# a = math.cos(math.pi/4)
# b = math.sin(math.pi/4)

# x_off = centrex - centrex * a + centrey * b+30
# y_off = centrey - centrex * b - centrey * a+30
# M = [5*a, -0.5*b, b, 1/2*a, x_off, y_off]

# rotated = affine_transform(polyg,M)
# x,y = rotated.exterior.coords.xy
# plt.plot(x,y, color='blue')



# print(rotated)




# M_matrix = [[M[0],M[1],M[4]],[M[2],M[3],M[5]],[0,0,1]]
# np_matrix = np.matrix(M_matrix)
# np_matrix_inverse = np.array(np_matrix.I)
# M_inverse = [np_matrix_inverse[0][0],np_matrix_inverse[0][1],np_matrix_inverse[1][0],np_matrix_inverse[1][1],np_matrix_inverse[0][2],np_matrix_inverse[1][2]]
# back = affine_transform(rotated,M_inverse)
# x,y = polyg.exterior.coords.xy
# plt.plot(x,y, color='black')
plt.axis('equal')
plt.savefig("polygon_before.png")

# print(back)

# x1,y1 = rotated.exterior.coords.xy
# plt.plot(x1,y1)
# plt.savefig("poly.png")