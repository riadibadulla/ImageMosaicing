import cv2
import numpy as np
import math

def drawImage(param,h2,w2,img2,img2_canvas_size):
        a,b,c,d,thetha,t_x,t_y = param
        thetha = thetha * math.pi/180
        r_cos = math.cos(thetha)
        r_sin = math.sin(thetha)
        centrex = img2_canvas_size/2
        centrey = img2_canvas_size/2

        vis2 = np.zeros((img2_canvas_size+6000,img2_canvas_size+6000,3), dtype=np.uint8)
        vis2[int((img2_canvas_size-h2)/2)+1000:1000+h2+int((img2_canvas_size-h2)/2), 
        1000+int((img2_canvas_size-w2)/2):1000+w2+int((img2_canvas_size-w2)/2),
        :3] = img2
        h,w = vis2.shape[:2]

        centrex1 = w/2
        centrey1 = h/2

        x_off = centrex1 - centrex * r_cos + centrey1 * r_sin + t_x
        y_off = centrey1 - centrex * r_sin - centrey1 * r_cos + t_y

        #M2 = np.float32([[a*r_cos,-b*r_sin, x_off],[c*r_sin,d*r_cos,y_off],[0,0,1]])
        M2 = np.float32([[0.5,0,0],[0,1,0],[0,0,1]])
        vis2 =cv2.warpPerspective(vis2,M2,(w,h))

        cv2.imwrite("transformedImage.jpg",vis2)
        #cv2.imshow('image',vis2)
        #cv2.waitKey(0)

img2 = cv2.imread('images/old_course.jpeg')
h2, w2 = img2.shape[:2]
img2_canvas_size = int(math.sqrt(math.pow(h2,2)+math.pow(w2,2)))
param = [1,1,1,1,72,0,0]
drawImage(param,h2,w2,img2,img2_canvas_size)
