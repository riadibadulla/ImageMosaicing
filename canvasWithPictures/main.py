import cv2
import numpy as np
import time 

def get_intersectionX(SHIFT,img1,img2,h1,h2):
    vis = np.zeros((max(h1, h2),SHIFT,3), dtype=np.float64)
    intersection = [vis,vis.copy]
    intersection[0] = img1[:h1,-SHIFT:]
    intersection[1] = img2[:h2,:SHIFT]
    return intersection

def get_intersectionY(SHIFT, intersectionX):
    intersection = np.array([intersectionX[0][:SHIFT][:][:],intersectionX[1][:SHIFT][:][:]])
    return intersection

def calculate_loss(intersection):
    loss = 0
    loss = np.mean(np.absolute(np.subtract(intersection[1],intersection[0])))
    return loss

SHIFT_X = 1
SHIFT_Y = 1

# Timing
START_TIME = time.time()

img1 = cv2.imread('/cs/home/ri31/project-scripts/canvasWithPictures/images/Map2.png')
img2 = cv2.imread('/cs/home/ri31/project-scripts/canvasWithPictures/images/Map1.png')  

h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]

intersection = get_intersectionX(1,img1,img2,h1,h2)
intersection = get_intersectionY(1,intersection)
minimum_loss = calculate_loss(intersection)
stageIsOneX = None

def optimise(stage):
    global stageIsOneX,minimum_loss,SHIFT_X,SHIFT_Y
    for i in range(1,min(w1,w2)):
        for j in range(1,min(h1,h2)+1):
            print("LoopX ",i+1)
            print("LoopY ",j+1)
            intersection = get_intersectionX(i,img1,img2,h1,h2)
            intersection = get_intersectionY(j,intersection)
            loss = calculate_loss(intersection)
            #print(SHIFT_Y)
            if  loss <= minimum_loss:
                print(loss)
                minimum_loss = loss
                SHIFT_X = i
                SHIFT_Y = j
                stageIsOneX = stage
                drawImage()

def getShift():
    global img1,img2,w1,w2
    optimise(True)
    img1,img2 = img2, img1
    w1,w2 = w2,w1
    optimise(False)
    if stageIsOneX:
        img1,img2 = img2, img1
        w1,w2 = w2,w1

def getImage():
    global img1,img2,h1,h2,w1,w2,SHIFT_X, SHIFT_Y
    print("ShiftX: ",SHIFT_X)
    print("ShiftY: ", SHIFT_Y)
    vis = np.zeros((h1+h2+300, w1+w2+300,3), np.uint8)
    vis[300:h1+300, 300:w1+300,:3] = img1
    vis[h1+300-SHIFT_Y:h2+h1-SHIFT_Y+300, w1-SHIFT_X+300:w1+w2-SHIFT_X+300,:3] = img2
    return vis


def drawImage():
    vis = getImage()
    cv2.imwrite("output.jpg",vis)
    cv2.imshow('image',vis)
    cv2.waitKey(10)

getShift()
vis = getImage()

print("Shift: ",SHIFT_X)
cv2.imwrite("output.jpg",vis)
cv2.imshow('image',vis)
# Timing
END_TIME = time.time()
print("Time taken: ", format(END_TIME - START_TIME), " seconds")
cv2.waitKey()

