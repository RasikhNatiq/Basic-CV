import cv2 #openCV digital image manipulation library
import face_recognition # digital image manipulation library used to make encodings of a face and compare faces
import os # stands for operating system used for handling directories
from datetime import datetime
import numpy as np #mathematics library
from mss import mss #Multiple ScreenShots it is for taking screen shots
from tkinter import *   #Graphical Library
import tkinter as tk
import threading # To perform multiprocessing

AttFile=tk.Tk() #creating GUI with tkinter
AttFile.title("Python Semester Project")
AttFile.configure(bg="#54FA9B")
AttFile.geometry("400x300")

with open("class Atttendance.txt", "r+") as file:
    file.truncate(0) # delete all records
path = 'images' # path to directory where images are stored
imagesList = []
classNames = []

def loadImages():
    global imagesList,classNames
    myList = os.listdir(path)   #get all the items from the directory
    for pic in myList:
        current_image = cv2.imread(f"{path}/{pic}") #getting image one by one
        imagesList.append(current_image)
        classNames.append(os.path.splitext(pic)[0]) #splitting name and extension of file

loadImages()

def getEncondings(images):
    encodedList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #converting image to RGB
        encodedList.append(face_recognition.face_encodings(img))    #getting face encodings of every image stored in the file
    return encodedList

encodedList = getEncondings(imagesList)

encodedList_className = {}
for encL, name in  zip(encodedList,classNames):
    encodedList_className.update({name : encL}) #creating a dictionary consists of student Names and their image encodings
print("Encoding Complete")

def mark_attendance(name):
    with open("class Atttendance.txt", "r+") as file:
        check = True
        lines = file.readlines()
        for line in lines:
            if name in line:
                check = False
                break
        if check:
            file.write(name)   #writing name in the destination file
            Time = datetime.now()
            time_string = Time.strftime('%H:%M:%S')
            file.write(" " + time_string + "\n")    #writting the attendance time in the destination file

bounding_box = {'top': 0, 'left': 0, 'width': 2400, 'height': 1800} #creating a bounding box inn which our buttons will show
screen = mss() #creating an instance of mss
switch = True
def grabScreen():
    while switch:
        sct_img = screen.grab(bounding_box) #recording the current screen showing
        imgS = cv2.resize(np.array(sct_img), (0, 0), None, 0.5, 0.5)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        all_imgLoc = face_recognition.face_locations(imgS)  #getting image locations on the screen
        for imgLoc in all_imgLoc:
            if imgLoc == []:
                continue
            imgenc = face_recognition.face_encodings(imgS, [imgLoc])    #getting the encodings of the images detected in the taken image
            dist = []
            for name,encoding in encodedList_className.items():
                match = face_recognition.compare_faces(encoding[0], imgenc,0.56)    #coparing two faces
                distance = face_recognition.face_distance(encoding[0], imgenc)  #Getting the diffrence between two images
                dist.append(distance)
                if match[0] == True:
                    idx = dist.index(distance[0])
                    name = classNames[idx].upper()
                    print(name)
                    mark_attendance(name)   #marks the attendance by calling the written function

def run():
    while (switch):
        grabScreen()
        if switch == False:
            break
def startTaking():
    thread = threading.Thread(target=run)   #performs multiple operations at the same time
    thread.start()                          #Here it uses multi threading for the buttons shown

def takeAttendance():
    global switch
    switch = True
    startTaking()

def stopAttendance():
    global switch
    switch = False

def exitInterface():
    AttFile.destroy()

label = Label(AttFile, text="Attendance Project", bg="#092521", fg="white", font=("Times",20 , "bold"), padx=40)
label.place(x= 45,y = 10)
take = tk.Button(AttFile, text="Take Attendance",fg="white", font=("Times",14 , "bold"), bg="#092521", command=takeAttendance)
take.place(x=120,y=110)
stop = tk.Button(AttFile, text="Stop Taking",fg="white", font=("Times",14 , "bold"), bg="#092521", command=stopAttendance)
stop.place(x=140,y=150)
killbutton = tk.Button(AttFile, text="EXIT",fg="white", font=("Times",14 , "bold"), bg="#092521", command=exitInterface)
killbutton.place(x=168,y=190)

#Creatiing and placing the buttoons and label in the plotted area

AttFile.mainloop() #calling the mainloop of ktinker file
