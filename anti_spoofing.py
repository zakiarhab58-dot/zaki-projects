import cv2 as cv
import dlib as db
import random
import numpy as np
texts=('close ur right eye','close ur left eye')
landmarks=db.shape_predictor("shape_predictor_68_face_landmarks.dat")
detector=db.get_frontal_face_detector()
change_action=True
ind=0
def check(frame,croped_body,yy,xx):
    global change_action
    global ind
    texts=("close ur left eye","close ur right eye")
    h,w=frame.shape[:2]
    h1,w1=croped_body.shape[:2]
    croped_body=cv.cvtColor(frame,cv.COLOR_RGB2GRAY)
    faces_=detector(croped_body)
    if len(faces_)==1:
        face_=faces_[0]
        landmarks_=landmarks(croped_body,face_)
        x_11,y_11=face_.left()+xx,face_.top()+yy
        x11,y11=x_11+(int(face_.right())-int(face_.left())),y_11+(int(face_.bottom())-int(face_.top()))
        cv.rectangle(frame,(x_11,y_11),(x11,y11),(0,255,0),2)
        if change_action==True:
            ind=random.randint(0,1)
            ind=0
            change_action=False
        if y_11>10:
            cv.putText(frame,texts[ind],(x_11,y_11-10),1,1,(0,255,0),2)
        else:
            cv.putText(frame,texts[ind],(x_11,y_11+10),1,1,(0,255,0),2)
        if ind==1:
            x, y = int((landmarks_.part(43).x + landmarks_.part(44).x) / 2), int(
                (landmarks_.part(43).y + landmarks_.part(44).y) / 2)
            x1, y1 = int((landmarks_.part(47).x + landmarks_.part(46).x) / 2), int(
                (landmarks_.part(47).y + landmarks_.part(46).y) / 2)
            distance = np.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
            x_, y_ = landmarks_.part(42).x, landmarks_.part(42).y
            x_1, y_1 = landmarks_.part(45).x, landmarks_.part(45).y
            distance_ = np.sqrt((x_1 - x_) ** 2 + (y_1 - y_) ** 2)
            pourcentage = distance * 100 / distance_
            x__, y__ = int((landmarks_.part(37).x + landmarks_.part(38).x) / 2), int(
                (landmarks_.part(37).y + landmarks_.part(38).y) / 2)
            x1___, y1___ = int((landmarks_.part(40).x + landmarks_.part(41).x) / 2), int(
                (landmarks_.part(40).y + landmarks_.part(41).y) / 2)
            distance__ = np.sqrt((x1___ - x__) ** 2 + (y1___ - y__) ** 2)
            xx_, yy_ = landmarks_.part(36).x, landmarks_.part(36).y
            xx_1, yy_1 = landmarks_.part(39).x, landmarks_.part(39).y
            distance___ = np.sqrt((xx_1 - xx_) ** 2 + (yy_1 - yy_) ** 2)
            pourcentage_ = distance__ * 100 / distance___
            print(pourcentage_,pourcentage)
            if pourcentage_-pourcentage>5:
                change_action=True
        elif ind==0:
            x, y = int((landmarks_.part(37).x + landmarks_.part(38).x) / 2), int(
                (landmarks_.part(37).y + landmarks_.part(38).y) / 2)
            x1, y1 = int((landmarks_.part(41).x + landmarks_.part(40).x) / 2), int(
                (landmarks_.part(41).y + landmarks_.part(40).y) / 2)
            distance = np.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
            x_, y_ = landmarks_.part(36).x, landmarks_.part(36).y
            x_1, y_1 = landmarks_.part(39).x, landmarks_.part(39).y
            distance_ = np.sqrt((x_1 - x_) ** 2 + (y_1 - y_) ** 2)
            pourcentage = distance * 100 / distance_
            x__, y__ = int((landmarks_.part(43).x + landmarks_.part(44).x) / 2), int(
                (landmarks_.part(43).y + landmarks_.part(44).y) / 2)
            x1___, y1___ = int((landmarks_.part(47).x + landmarks_.part(46).x) / 2), int(
                (landmarks_.part(47).y + landmarks_.part(46).y) / 2)
            distance__ = np.sqrt((x1___ - x__) ** 2 + (y1___ - y__) ** 2)
            xx_, yy_ = landmarks_.part(42).x, landmarks_.part(42).y
            xx_1, yy_1 = landmarks_.part(45).x, landmarks_.part(45).y
            distance___ = np.sqrt((xx_1 - xx_) ** 2 + (yy_1 - yy_) ** 2)
            pourcentage__ = distance__ * 100 / distance___
            print(pourcentage__, pourcentage)
            if pourcentage__-pourcentage>5:
                change_action = True
    if change_action==True:
        return True
    else:
        return False