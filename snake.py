import cv2
import imutils
from collections import deque
import numpy as np
import time

score = 0
max_score=5
list_capacity = 0
max_lc =20
l = []
flag=0
apple_x = None
apple_y = None
center = None

def dist(pt1,pt2):
    return np.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)
cap = cv2.VideoCapture(0)

while 1:

    ret,frame = cap.read()
    
    img = imutils.resize(frame.copy(), width=550)

    img = cv2.GaussianBlur(img,(11,11),0)          
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)     
    
    if apple_x is None or apple_y is None:
        
        
        apple_x = np.random.randint(30,frame.shape[0]-30) 
        apple_y = np.random.randint(100,350)       

    cv2.circle(frame,(apple_x,apple_y),3,(0,0,255),-1)
    
    blueLower = (90, 50, 50)
    blueUpper = (130, 255, 255)
 
    mask = cv2.inRange(img, blueLower, blueUpper)
    mask = cv2.erode(mask,None,iterations=2)
    mask = cv2.dilate(mask,None,iterations=2)
  
    cnts = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    
    if len(cnts)>0:
        ball_cont = max(cnts,key=cv2.contourArea)
        (x,y),radius = cv2.minEnclosingCircle(ball_cont)
        center = (int(x), int(y))

        
        if radius>10:
            cv2.circle(frame,center,5,(0,0,255),3)
            
            if len(l)>list_capacity:
                l = l[1:]
            
            if prev_c and (dist(prev_c,center) >3.5):
                l.append(center)
                
            apple = (apple_x,apple_y)
            if dist(apple,center)<15:
                score+=1
                if score==max_score:
                    flag=1
                list_capacity+=1
                apple_x = None
                apple_y = None
        
    for i in range(1,len(l)):
        if l[i-1] is None or l[i] is None:
            continue
        r,g,b = np.random.randint(0,255,3)
        
        cv2.line(frame,l[i],l[i-1],(int(r),int(g),int(b)), thickness = int(len(l)/max_lc+2)+2)    
    
    
    cv2.putText(frame,'Score :'+str(score),(450,100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
    if flag==1:
        cv2.putText(frame,'YOU WIN !!',(100,250),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),3)
        
    cv2.imshow('live feed',frame)
    cv2.imshow('mask',mask)
    prev_c = center
    
    if cv2.waitKey(1)==27:
        break
        
cv2.destroyAllWindows()
cap.release()
