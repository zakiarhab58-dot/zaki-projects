import os
from anti_spoofing import *
from anti_spoofing import check
import random
import cv2 as cv
import face_recognition as fc
import time
from ultralytics import YOLO
from twilio.rest import Client
import math
from decimal import Decimal,getcontext
from datetime import datetime
import dlib as db
code='1234'
getcontext().prec=50
yolo_model_name='yolo26n.pt'
model=YOLO(yolo_model_name)
video_path='video_.MOV'
video=cv.VideoCapture(video_path)
account_sid = ""
auth_token = ""
client=Client(account_sid,auth_token)
file_name=r'workers.yaml'
file_path=r'C:\Users\sim\Pictures\attendance system'
yolo = YOLO('yolo26n.pt')
def send_message(client,message,from_,to_):
    try:
        sent=client.messages.create(
            to=to_,
            from_=from_,
            body=message,
        )
    except:
        print('error sending message')
def create_filecsv(file_path,file_name):
    if not os.path.exists(os.path.join(file_path,file_name)):
        with open(os.path.join(file_path,file_name),'w') as file:
            file.write('date,name,time,late_or_no,late_times\n')
create_filecsv(r'C:\Users\sim\Pictures\attendance system','arrivals.txt')
def add_to_filecsv(file_path,file_name,date,name,time,late_or_no,late_times):
    if os.path.exists(os.path.join(file_path,file_name)):
        with open(os.path.join(file_path,file_name),'a') as file:
            file.write(f'{date},{name},{time},{late_or_no},{late_times}\n')
def get_encoded_list(file_path,encoded_file_name,file_name):
    with open(os.path.join(file_path,encoded_file_name,file_name),'r') as file:
        encoded_list=file.readline()
        seperated_list=encoded_list.split(' ')
        int_seperated_list=[]
        for number in seperated_list:
            try:
                int_seperated_list.append(Decimal(number))
            except:
                continue
        return int_seperated_list
def get_encoded_list0(encoded):
    int_list=[]
    for list in encoded:
        for number in list:
            int_list.append(number)
    return int_list
def comparison(encoded_list1,encoded_list2):
    if len(encoded_list1)==len(encoded_list2):
        addition=0
        for index in range(0,len(encoded_list1)):
            final_number=(encoded_list1[index]-float(encoded_list2[index]))**2
            addition+=final_number
        return math.sqrt(addition)
def decide(result_of_comparison,tolerance):
    if tolerance<1:
        if result_of_comparison<tolerance:
            return True
        else:
            return False
def get_name(file_path,file_name_dict,index):
    file=os.path.join(file_path,file_name_dict)
    with open(file,'r') as file:
        for line in file.readlines():
            list=line.split(',')
            if str(list[1])==str(index)+'\n':
                return str(list[0])
def make_encoded_file(file_path,encoded_file_name,encoded_list):
    file_name=str(int(time.time()))+".txt"
    with open(os.path.join(file_path,encoded_file_name,file_name),'w') as file:
        for real_list in encoded_list:
            for number in real_list:
                file.write(f'{number} ')
def delete_main(file_path,encoded_faces_file_name,faces_file_name,dict_file_name):
    name=str(input('enter the name : ')).lower()
    names=[]
    number=[]
    with open(os.path.join(file_path,dict_file_name),'r') as file:
        lines=file.readlines()
        for x,line in enumerate(lines):
            list_=line.split(',')
            if list_[0]==name:
                for n,image in enumerate(os.listdir(os.path.join(file_path,faces_file_name))):
                    if n==x:
                        os.remove(os.path.join(file_path,faces_file_name,image))
                for n,encoded_image in enumerate(os.listdir(os.path.join(file_path,encoded_faces_file_name))):
                    if n==x:
                        os.remove(os.path.join(file_path,encoded_faces_file_name,encoded_image))
            else:
                names.append(list_[0])
                number.append(list_[1][0])
    os.remove(os.path.join(file_path,dict_file_name))
    with open(os.path.join(file_path,dict_file_name),'w') as file:
        for x,name in enumerate(names):
            file.write(f'{name},{number[x]}\n')

def make_diction_and_add(file_path,file_name_dict,workers_name):
    file=os.path.join(file_path,file_name_dict)
    if not os.path.exists(file):
        with open(file,'w') as file:
            file.write(f'{workers_name},{len(os.listdir(os.path.join(file_path,'faces')))-1}\n')
    else:
        with open(file,'a') as file:
            file.write(f'{workers_name},{len(os.listdir(os.path.join(file_path,'faces')))-1}\n')
def register_face(file_path,file_name_faces,face_image,face_image_name):
    final_name=str(face_image_name)+'.jpg'
    cv.imwrite(os.path.join(file_path,file_name_faces,final_name),face_image)
def add_proccess_main(file_path,file_name_dict,file_name_faces,face_image_name):
    cv.destroyAllWindows()
    how_many=input('How many people do you want to add? ')
    try :
        nm=int(how_many)
        for _ in range(0,nm):
            while True:
                ret_,frame_=video.read()
                frame=frame_.copy()
                frame=cv.flip(frame,1)
                frame___=frame.copy()
                frame_=cv.cvtColor(frame_,cv.COLOR_BGR2RGB)
                frame_=cv.flip(frame_,1)
                frame_=cv.resize(frame_,(640,480))
                faces=fc.face_locations(frame_)
                if len(faces)>1:
                    cv.putText(frame,'ONLY ONE FACE',(20,100),1,1,(0,0,255),2)
                elif len(faces)==1:
                    cv.putText(frame, 'STAND STILL', (20, 100), 1, 1, (0, 0, 255), 2)
                    y,x1,y1,x=map(int,faces[0])
                    face__=frame___[y-100:y1+50,x-20:x1+20]
                    cv.rectangle(frame,(x,y),(x1,y1),(0,0,255),2)
                cv.imshow('Video',frame)
                key=cv.waitKey(1)
                if key==ord('q') and len(faces)==1:
                    cv.destroyAllWindows()
                    workers_name=str(input('Enter your name: '))
                    register_face(file_path,file_name_faces,face__,face_image_name)
                    list=fc.face_encodings(frame_,[faces[0]])
                    make_encoded_file(file_path,'encoded',list)
                    make_diction_and_add(file_path, file_name_dict, workers_name)
                    break
    except:
        print('Please enter a number')
checked_people_id=[]
while True:
    ret,picture=video.read()
    if not ret:
        break
    else:
        picture=cv.flip(picture,1)
        picture=cv.resize(picture,(640,480))
        picture_cop=picture.copy()
        tracking_results=model.track(picture,persist=True,classes=[0])[0]
        if len(tracking_results)>0:
            for body in tracking_results:
                if body.boxes is not None:
                    if body.boxes.id[0].item() not in checked_people_id:
                        x,y,x1,y1=map(int,body.boxes.xyxy[0].tolist())
                        croped_body=picture[y:y1,x:x1]
                        croped_body=cv.cvtColor(croped_body,cv.COLOR_BGR2RGB)
                        faces=fc.face_locations(croped_body)
                        print(len(faces))
                        if len(faces)==1:
                            decition=check(picture_cop,croped_body,x,y)
                            if decition==True:
                                checked_people_id.append(body.boxes.id[0].item())
                                face=faces[0]
                                encoded=fc.face_encodings(croped_body,[face])
                                list0=get_encoded_list0(encoded)
                                for x,file in enumerate(os.listdir(os.path.join(r'C:\Users\sim\Pictures\attendance system','encoded'))):
                                    list1=get_encoded_list(r'C:\Users\sim\Pictures\attendance system','encoded',file)
                                    result__=comparison(list0,list1)
                                    tolerance=0.6
                                    if decide(result__,tolerance)==True:
                                        name=get_name(r'C:\Users\sim\Pictures\attendance system','dict.txt',x)
                                        date=datetime.now().strftime('%Y-%m-%d')
                                        time=datetime.now().strftime('%H:%M:%S')
                                        add_to_filecsv(r'C:\Users\sim\Pictures\attendance system','arrivals.txt',date,name,time,'yes','1')
                                        print(name,'access not denied')
                                    else:
                                        print('access denied')
        cv.imshow('picture',picture_cop)
        key=cv.waitKey(1)
        if key==ord('q'):
            break
        elif key==ord('a'):
            cv.destroyAllWindows()
            code_=input('Enter your code: ')
            if code_==code:

                add_proccess_main(r'C:\Users\sim\Pictures\attendance system','dict.txt','faces',str(int(time.time())))
        elif key==ord('w'):
            cv.destroyAllWindows()
            code_ = input('Enter your code: ')
            if code_ == code:
                delete_main(r'C:\Users\sim\Pictures\attendance system','encoded','faces','dict.txt')



