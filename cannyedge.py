import cv2
import numpy as np

img = cv2.imread('sample.png',0)#Replace sample.png with the picture name in your same folder
edges = cv2.Canny(img,100,200)

cv2.imshow('result',edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
