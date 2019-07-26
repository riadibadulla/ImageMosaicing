from ImageStitcher import ImageStitcher
import cv2

img1 = cv2.imread('images/Map1-rotate.png')
img2 = cv2.imread('images/Map2.png')  

x0 = [1,2,2,1,0,120,100,1,1,1,1,-45,0,0]
stitcher =ImageStitcher(img1,img2,False)
stitcher.test_one_iter(x0)



# rectangle = [(174.0, 281.0), (279.0, 281.0), (279.0, 192.0), (271.0, 184.0), (174.0, 281.0)]
# polygon = Polygon(rectangle)
# x,y = polygon.exterior.coords.xy
# plt.plot(x,y)
# bounds = polygon.bounds
# height = int(bounds[3]) - int(bounds[1])
# width = int(bounds[2]) - int(bounds[0])
# p = Path(rectangle)
# x, y = np.meshgrid(np.arange(400), np.arange(400)) # make a canvas with coordinates
# x, y = x.flatten(), y.flatten()
# points = np.vstack((y,x)).T

# grid = p.contains_points(points)
# mask = grid.reshape(400,400)
# coords = np.nonzero(mask)
# coords = np.array(coords)
# coordsInTupples = list(tuple(map(tuple, coords.transpose())))
# #end = time.time()
# #print("geting the coornates: ",end-Start,"\n\n" )
# l = LineString(coordsInTupples)
# x,y = l.coords.xy
# plt.scatter(x,y)
# plt.savefig("insidePolygon.png")