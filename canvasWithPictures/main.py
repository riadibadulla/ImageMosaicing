import cv2
import numpy as np
import time 

def get_intersection(SHIFT,img1,img2,h1,h2):
    vis = np.zeros((max(h1, h2),SHIFT,3), dtype=np.uint8)
    intersection = [vis,vis.copy]
    intersection[0] = img1[:h1,-SHIFT:]
    intersection[1] = img2[:h2,:SHIFT]
    return intersection


def calculate_loss(intersection):
    loss = 0
    loss = np.sum(np.absolute(np.subtract(intersection[1],intersection[0])))
    return loss

SHIFT_CONST = 1

# Timing
START_TIME = time.time()

img1 = cv2.imread('/cs/home/ri31/project-scripts/canvasWithPictures/images/Map1.png')
img2 = cv2.imread('/cs/home/ri31/project-scripts/canvasWithPictures/images/Map2.png')  

h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]

oldMax = calculate_loss(get_intersection(SHIFT_CONST,img1,img2,h1,h2))/(SHIFT_CONST*h1)
maxShift = 1
for i in range(2,100):
    print("Loop ",i+1)
    intersection = get_intersection(i,img1,img2,h1,h2)
    loss = calculate_loss(intersection)/(i*h1)
    if  loss < oldMax:
        oldMax = loss
        maxShift = i
SHIFT_CONST = maxShift


vis = np.zeros((max(h1, h2), w1+w2,3), np.uint8)
vis[:h1, :w1,:3] = img1
vis[:h2, w1-SHIFT_CONST:w1+w2-SHIFT_CONST,:3] = img2

print("Shift: ",SHIFT_CONST)
cv2.imwrite("output.jpg",vis)
cv2.imshow('image',vis)
# Timing
END_TIME = time.time()
print("Time taken: ", format(END_TIME - START_TIME), " seconds")
cv2.waitKey()

