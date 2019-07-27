from ImageStitcher import ImageStitcher
import cv2

img1 = cv2.imread('images/Map1-rotate.png')
img2 = cv2.imread('images/Map2.png')  

x0 = [0.67811993, 0.46246523, 0.2639719 , 0.05067076, 0.01803103, 0.12002536,
 0.58894882 ,0.71443625 ,0.66426334 ,0.38575423, 0.29171836, 0.56493315,
 0.187759,   0.26246541]

stitcher =ImageStitcher(img1,img2,False)
stitcher.set_canvas()
stitcher.test_one_iter(x0)
stitcher.drawImage(x0,0)



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