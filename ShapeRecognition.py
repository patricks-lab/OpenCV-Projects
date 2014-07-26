import cv2
import numpy as np
import time
import math
import sys

cap = cv2.VideoCapture(0)
sizeMax = 0
blueSizeMax = 0

def PColor(array):
    array2 = [0,0,0]
    array2[0] = array[0] / 2
    array2[1] = array[1]*255/100
    array2[2] = array[2]*255/100
    return array2

def distance(x1,y1,x2,y2):
    return math.sqrt( (x2-x1)**2 + (y2-y1)**2)
    

while(1):
    sizeMax = 0
    blueSizemax = 0
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

 #   hsv = cv2.bilateralFilter(hsv_beforefilter,9,75,75)
    
    #Erosion+dilation to remove noise
    element = np.ones((5,5)).astype(np.uint8)
    hsv = cv2.erode(hsv,element)
    hsv = cv2.dilate(hsv,element)

    # define range of BLUE color in HSV
    lower_blue = np.array([80, 50,  50])
    upper_blue = np.array([130, 255, 255])

     # Threshold the HSV image to get only blue colors
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)


    contours, hierarchy = cv2.findContours(blue_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame,contours,-1,(0,255,0),3)
    
    for i in range(len(contours)):

      #print contours[i]
        
      #CHeck for the BIGGEST Contour.
      if(len(contours[i]) > blueSizeMax):
          blueSizeMax = i
            

    #print sizeMax, blueSizeMax
    
    #print(blueSizeMax)
    
        
    try:#CATCH ALL divide-by 0 and index-out of bound errors!!!

     
 #       font = cv2.FONT_HERSHEY_PLAIN
#        cv2.putText(img,str(centroid_x),(20,20), font, 4,(255,255,255),2,cv2.LINE_AA)
#        cv2.putText(img,str(centroid_y),(60,60), font, 4,(255,255,255),2,cv2.LINE_AA)
        
        #BLUE contours
        (x_2,y_2),radius_2 = cv2.minEnclosingCircle(contours[blueSizeMax])
        center = (int(x_2),int(y_2))
        radius_2 = int(radius_2)
        cv2.circle(frame,center,radius_2,(0,255,0),2)
        cv2.drawContours(frame,contours, blueSizeMax,(0,0,255),3)

        #DRAW the biggest BLUE contour's centre
        M=cv2.moments(contours[blueSizeMax])
        blue_centroid_x = int(M['m10']/M['m00'])
        blue_centroid_y = int(M['m01']/M['m00'])
        cv2.circle(frame,(blue_centroid_x, blue_centroid_y),5,(0,0,255))

        #Only check if contour-size is greater than 30-to reduce noise
        if(cv2.contourArea(contours[blueSizeMax]) > 30):
            #get 3% of arc to set epsilon
            #also find the approximate of points/sides of the poly-gon
            approx = cv2.approxPolyDP(contours[blueSizeMax],0.03*cv2.arcLength(contours[blueSizeMax],True),True)
            #print("Size Of Blue = " + str(len(approx) ) )
            if(len(approx) == 3):
                print("Triangle")
            elif(len(approx) == 4):
                print("Quadrilateral")
            elif(len(approx) == 5):
                print("Pentagon")
            elif(len(approx) == 6):
                print("Hexagon")
            elif(len(approx)== 8):
                print("Octagon")
            else:
                print("Size Of Blue = " + str(len(approx) ) )

        
    except Exception,e:
        #print e
        pass
        
   
    #print(len(contours_orange))
    cv2.imshow('frame',frame)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    #time.sleep(0.5)

cv2.destroyAllWindows()
