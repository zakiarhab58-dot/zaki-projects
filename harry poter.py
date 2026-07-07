import cv2 as cv
import numpy as np
background=0
fps=0
video=cv.VideoCapture(0)
while True:
    ret,frame=video.read()
    if not ret:
        break
    else:
        frame=cv.flip(frame,1)
        frame=cv.resize(frame,(640,480))
        if fps==0:
            background=frame
        frame_=frame.copy()
        frame=cv.cvtColor(frame,cv.COLOR_BGR2HSV)
        max_color=np.array([90,50,50])
        min_color=np.array([130,255,255])
        mask=cv.inRange(frame,max_color,min_color)
        cv.imshow('Video',mask)
        for row in range(0,mask.shape[0]):
            for col in range(0,mask.shape[1]):
                if mask[row][col]==255:
                    frame_[row][col]=background[row][col]
        fps+=1
        cv.imshow('Video',frame_)
        key=cv.waitKey(1)
        if key==ord('q'):
            break
