import cv2
import numpy as np

img = cv2.imread('/cs/home/ri31/project-scripts/canvasWithPictures/images/andrews.jpg',0)
cv2.imshow('image',img)
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
print(img)