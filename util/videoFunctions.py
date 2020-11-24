import cv2
import face_recognition
import numpy as np
import os

# делаем фото юзера
def takePicture(photoName):
    cap = cv2.VideoCapture(0)

    while True:
        if cap.isOpened():
            check, frame = cap.read()
            faceLoc = face_recognition.face_locations(frame)
            if faceLoc:
                frameSelectedFace = cv2.rectangle(frame,(faceLoc[0][3],faceLoc[0][0]),(faceLoc[0][1],faceLoc[0][2]),(0,255,0),1)
                cv2.imshow("Video", frameSelectedFace)
            cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("Biometrics/photo/"+photoName+".jpeg", frame)
            cv2.destroyWindow("Video")
            break

# энкодируем фото и сохраняем
def saveEncode(photoName):
    photo = face_recognition.load_image_file("Biometrics/photo/"+photoName+".jpeg")
    photo = cv2.cvtColor(photo,cv2.COLOR_BGR2RGB)
    # faceLoc = face_recognition.face_locations(photo)[0]
    encode = face_recognition.face_encodings(photo)[0]
    np.savetxt("Biometrics/encode/"+photoName+".csv", encode)

# загружаем все сохранёные энкоды в один массив
def uploadEncode():
    encodeList =[]
    path = "Biometrics/encode"
    filesList = os.listdir(path)
    for x in filesList:
        # print(x)
        encodeList.append(np.loadtxt("Biometrics/encode/"+x))
    return encodeList