poverhnost = input("Введите поверхность: ")
diametr = input("Введите диаметр: ")
tolshina = input("Введите толщину: ")
koli4estvo = input("Введите кол-во: ")
adress = input("adress")

print("poverhnost/diametr/tolshina/koli4estvo/adress")
print(poverhnost+diametr+tolshina+"/"+koli4estvo+"/"+adress)










































# import datetime
# import numpy as np
# import cv2
# import face_recognition
#
# from util import functions
# from entities import Attendance
# from entities import Notification
# from entities import Biometrics
#
# # Задаём кабинет где находиться камера
# defaultClassroom = "VK44"
#
# # Текущие дата и время
# date_now = datetime.datetime.now().date()
# time_now = datetime.datetime.now().time()
# # раскоментировать в случае теста
# date_now = datetime.date(2020, 9, 7)
# time_now = datetime.time(11,11,16)
#
#
# # подключаемся к базе данных
# db, cursor = functions.connect()
#
# # Получаем из базы данных ID нашего кабинета
# sql = "SELECT classroomID FROM Classroom WHERE address='" + defaultClassroom + "'"
# cursor.execute(sql)
# classroomID = cursor.fetchall()
# classroomID = classroomID[0][0]
# print(classroomID)
#
# cap = cv2.VideoCapture(0)
#
# usersUnknown = []
# usersUnknownName = []
# i=0
#
#
#
# # Добавляем в массив usersAccessDenied ID всех пользователей из базы данных
# usersAccessDenied = []
# sql = "SELECT userID FROM Users"
# cursor.execute(sql)
# uAD = cursor.fetchall()
#
# for x in uAD:
#     usersAccessDenied.append(x[0])
#
# usersAccessApproved = []
# update = 0
#
#
# while True:
# # --------------------------------------------------------------------------------------------------------------
#     # Получаем из базы данных временные промежутки в которые проводятся уроки,
#     # значения возвращаются как массив элементов timedelta
#     sql = "SELECT time_start, time_end FROM PartOfDay WHERE date='" + str(date_now) + "' AND classroomID = '"+str(classroomID)+"'"
#     cursor.execute(sql)
#     times = cursor.fetchall()
#
#     # # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#     # time_0 время 00:00:00 необходимо чтобы из элемента timedelta
#     # получть элемент времени
#     time_0 = datetime.time(0)
#     # t_delta элемент timedelta, который искользуется с целью указать, за сколько до начала пары
#     # начать отмечать приходящих
#     t_delta = datetime.timedelta(minutes=15)
#
#     # Проходим через все временные промежутки сравнивая их с текущим временем
#     # с целью выявить текущую пару
#     for start, end in times:
#         # Конвертируем элементы timedelta из массива в элементы времени
#         s_t = (datetime.datetime.combine(datetime.date(1,1,1),time_0) + start-t_delta).time()
#         e_t = (datetime.datetime.combine(datetime.date(1,1,1),time_0) + end).time()
#
#         # Получаем partofdayID, запрос в базу данных по дню (сегодня), кабинету (текущему), времени окончания урока
#         if s_t < time_now and e_t > time_now:
#             sql = "SELECT partofdayID FROM PartOfDay WHERE date='" + str(date_now) + "' AND classroomID = '" + str(
#                 classroomID) + "' AND time_end= '"+str(e_t)+"'"
#             cursor.execute(sql)
#             partofdayID = cursor.fetchall()
#             partofdayID = partofdayID[0][0]
#             timeLimit = e_t
#
#
#
#
#     # ------------------------------------------------------------------------------------------------------------pppppppppppppppppppppppppppppppppppppppppppp
#             if update == 0:
#                 # Добавляем в массив usersAccessApproved ID преподователя, через запрос к базе данных, к таблице
#                 # PartOfDay через partofdayID
#
#
#                 sql = "SELECT userID FROM PartOfDay WHERE partofdayID='" + str(partofdayID) + "'"
#                 cursor.execute(sql)
#                 teacherID = cursor.fetchall()
#                 usersAccessApproved.append(teacherID[0][0])
#
#                 # Получаем timetableID, расписание к которому относится наша пара,
#                 # для каждой группы оно уникальное
#                 sql = "SELECT timetableID FROM PartOfDay WHERE partofdayID='" + str(partofdayID) + "'"
#                 cursor.execute(sql)
#                 timetableID = cursor.fetchall()
#                 timetableID = timetableID[0][0]
#
#                 # Получаем ID группы у которой проходит пара по timetableID
#                 sql = "SELECT groupID FROM Timetables WHERE timetableID='" + str(timetableID) + "'"
#                 cursor.execute(sql)
#                 groupID = cursor.fetchall()
#                 groupID = groupID[0][0]
#
#                 # Получаем ID пользователей из этой группы
#                 sql = "SELECT userID FROM GroupesUsers WHERE groupID='" + str(groupID) + "'"
#                 cursor.execute(sql)
#                 userID = cursor.fetchall()
#
#                 # Додавляем ID всех пользователей в массив usersAccessApproved
#                 for x in userID:
#                     usersAccessApproved.append(x[0])
#                 print("usersAccessApproved"+ str(usersAccessApproved))
#
#                 # Так как на данный момент в массиве usersAccessDenied буквально все пользователи системы,
#                 # то убираем из него ID пользователей, которые в массиве usersAccessApproved.
#                 # Таким образом получаем 2 массива, пользователей которым доступ открыт и противоложный.
#                 for x in usersAccessApproved:
#                     usersAccessDenied.remove(x)
#                 update = 1
#                 # ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#
#     # ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
#
#
#     # ---------------------------------------------------------------------------------------------------------------------++++++++++++++++++++++++++++++++++++++++++++++
#     if time_now == timeLimit:
#         # Добавляем в массив usersAccessDenied ID всех пользователей из базы данных
#         usersAccessDenied = []
#         sql = "SELECT userID FROM Users"
#         cursor.execute(sql)
#         uAD = cursor.fetchall()
#
#         for x in uAD:
#             usersAccessDenied.append(x[0])
#
#         usersAccessApproved = []
#         i=0
#         usersUnknown = []
#         usersUnknownName = []
#         usersAccessDeniedEcodePath  = []
#         usersAccessApprovedEncodePath  = []
#         usersAccessDeniedEcode  = []
#         usersAccessApprovedEncode  = []
#
#     # Пути к файлам содержащих биометрические данные пользователя
#     usersAccessDeniedEcodePath = Biometrics.Biometrics().getEncodePath(usersAccessDenied)
#     if usersAccessApproved:
#         usersAccessApprovedEncodePath = Biometrics.Biometrics().getEncodePath(usersAccessApproved)
#
#
#     # биометрические данные пользователей
#     usersAccessDeniedEcode = Biometrics.Biometrics().uploadEncodeByPath(usersAccessDeniedEcodePath)
#     if usersAccessApproved:
#         usersAccessApprovedEncode = Biometrics.Biometrics().uploadEncodeByPath(usersAccessApprovedEncodePath)
#
#
#
#
#
#
#
#
#
#     check, frame = cap.read()
#     # frameS = cv2.resize(frame, (0, 0), None, 0.5, 0.5)
#     frameS = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
#
#     facesCurFrame = face_recognition.face_locations(frameS)
#     encodesCurFrame = face_recognition.face_encodings(frameS,facesCurFrame)
#
#
#
#     if usersAccessApproved:
#         for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
#             matchesApproved = face_recognition.compare_faces(usersAccessApprovedEncode,encodeFace)
#             faceDisApproved = face_recognition.face_distance(usersAccessApprovedEncode,encodeFace)
#
#             matchIndexApproved = np.argmin(faceDisApproved)
#
#             if matchesApproved[matchIndexApproved]:
#                 name = usersAccessApproved[matchIndexApproved]
#                 print(name)
#                 y1,x2,y2,x1 = faceLoc
#                 print(y1,x2,y2,x1)
#                 # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
#                 frame = cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),1)
#                 cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
#                 cv2.putText(frame,str(name),(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
#                 # --------------------------------------------------------------------------------------------------------------------------------
#                 attendance = Attendance.Attendance()
#                 attendance.attendanceRegistration(name, partofdayID, timeLimit)
#                 attendance.markAttendance()
#                 db.reconnect()
#                 message = "Approved"
#                 notification = Notification.Notification()
#                 notification.notificationRegistration(partofdayID, message)
#                 notification.diseaseCheck(name,frame)
#                 notification.lateCheck(name,frame)
#                 # markAttend(name)
#             elif len(matchesApproved) != len(facesCurFrame):
#
#                 # for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
#                 matchesDenied = face_recognition.compare_faces(usersAccessDeniedEcode, encodeFace)
#                 faceDisDenied = face_recognition.face_distance(usersAccessDeniedEcode, encodeFace)
#
#                 matchIndexDenied = np.argmin(faceDisDenied)
#                 if matchesDenied[matchIndexDenied]:
#                     name = usersAccessDenied[matchIndexDenied]
#                     print(name)
#                     y1, x2, y2, x1 = faceLoc
#                     print(y1, x2, y2, x1)
#                     # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
#                     frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
#                     cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
#                     cv2.putText(frame, str(name), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
#
#                     message = "Denied"
#                     notification = Notification.Notification()
#                     notification.notificationRegistration(partofdayID, message)
#                     notification.diseaseCheck(name,frame)
#                     notification.excessCheck(name,frame)
#
#                 elif usersUnknown:
#                     matchesUnknown = face_recognition.compare_faces(usersUnknown, encodeFace)
#                     faceDisUnknown = face_recognition.face_distance(usersUnknown, encodeFace)
#
#                     matchIndexUnknown = np.argmin(faceDisUnknown)
#                     if matchesUnknown[matchIndexUnknown]:
#                         name = usersUnknownName[matchIndexUnknown]
#                         print(name)
#                         y1, x2, y2, x1 = faceLoc
#                         print(y1, x2, y2, x1)
#                         # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
#                         frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
#                         cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
#                         cv2.putText(frame, str(name), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
#
#                         message = "UNKNOWN"
#                         notification = Notification.Notification()
#                         notification.notificationRegistration(partofdayID, message)
#                         notification.unknownCheck(name,frame)
#
#
#                     else:
#                         i+=1
#                         usersUnknownName.append("UNKNOWN "+str(i))
#                         usersUnknown.append(encodeFace)
#                         print("unknown+")
#                 else:
#                     i+=1
#                     usersUnknownName.append("UNKNOWN "+str(i))
#                     usersUnknown.append(encodeFace)
#
#
#                     print("unknown/////////////////////////////////////////////////////")
#     else:
#         for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
#
#                 # for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
#             matchesDenied = face_recognition.compare_faces(usersAccessDeniedEcode, encodeFace)
#             faceDisDenied = face_recognition.face_distance(usersAccessDeniedEcode, encodeFace)
#
#             matchIndexDenied = np.argmin(faceDisDenied)
#             if matchesDenied[matchIndexDenied]:
#                     name = usersAccessDenied[matchIndexDenied]
#                     print(name)
#                     y1, x2, y2, x1 = faceLoc
#                     print(y1, x2, y2, x1)
#                     # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
#                     frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
#                     cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
#                     cv2.putText(frame, str(name), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
#
#                     # message = "Denied"
#                     # notification = Notification.Notification()
#                     # notification.notificationRegistration(partofdayID, message)
#                     # notification.diseaseCheck(name)
#                     # notification.excessCheck(name)
#
#             elif usersUnknown:
#                 matchesUnknown = face_recognition.compare_faces(usersUnknown, encodeFace)
#                 faceDisUnknown = face_recognition.face_distance(usersUnknown, encodeFace)
#
#                 matchIndexUnknown = np.argmin(faceDisUnknown)
#                 if matchesUnknown[matchIndexUnknown]:
#                         name = usersUnknownName[matchIndexUnknown]
#                         print(name)
#                         y1, x2, y2, x1 = faceLoc
#                         print(y1, x2, y2, x1)
#                         # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
#                         frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
#                         cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
#                         cv2.putText(frame, str(name), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
#
#                         # message = "UNKNOWN"
#                         # notification = Notification.Notification()
#                         # notification.notificationRegistration(partofdayID, message)
#                         # notification.unknownCheck(name)
#
#
#                 else:
#                         i += 1
#                         usersUnknownName.append("UNKNOWN " + str(i))
#                         usersUnknown.append(encodeFace)
#                         print("unknown+")
#             else:
#                     i += 1
#                     usersUnknownName.append("UNKNOWN " + str(i))
#                     usersUnknown.append(encodeFace)
#
#                     print("unknown/////////////////////////////////////////////////////")
#
#                     # UNKNOWN = "UNKNOWN"
#                     # y1,x2,y2,x1 = faceLoc
#                     # print(y1,x2,y2,x1)
#                     # # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
#                     # frame = cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),1)
#                     # cv2.rectangle(frame,(x1,y2-35),(x2,y2),(255,0,0),cv2.FILLED)
#                     # cv2.putText(frame,UNKNOWN,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
#     cv2.imshow("okno", frame)
#     cv2.waitKey(100)
#




































# usersAccessDenied.remove(usersAccessApproved[0])
# print(usersAccessDenied)







# -----------------------------------------------------------------------------------------------------
# path = 'users_photo'
# myList = os.listdir(path)
# images = []
# className = []
# print(myList)
# for cl in myList:
#     curImg = cv2.imread(f'{path}/{cl}')
#     images.append(curImg)
#     className.append(os.path.splitext(cl)[0])
# print(className)
#
# def findEncodings(images):
#     encodeList = []
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = fr.face_encodings(img)[0]
#         encodeList.append(encode)
#     return encodeList
#
#
# def markAttend(name):
#     with open("Attend.csv","r+") as f:
#         myDataList = f.readlines()
#         nameList = []
#         for line in myDataList:
#             entry = line.split(",")
#             nameList.append(entry[0])
#         if name not in nameList:
#             now = datetime.now()
#             dtString =now.strftime("%H:%M:%S")
#             f.writelines(f'\n{name},{dtString}')
#
#
# encodeListKnown = findEncodings(images)
# print("encode complete")
#---------------------------------------------------------------------------------------------------------------------------
# cap = cv2.VideoCapture(0)
# cap.set(3,1500)
# cap.set(4,900)
# img = cv2.imread('users_photo/babyFOX.jpg')
# img2 = cv2.imread('users_photo/Kirill.jpg')
# print(img2.shape)
#
# i=0
# facesCurFrame = fr.face_locations(img)
# encodesCurFrame = fr.face_encodings(img, facesCurFrame)
# while True:--------------------------------------------------------------------------------------------------------------+
#     check, frame = cap.read()
#     frameS = cv2.resize(frame,(0,0),None,0.25,0.25)
#     frameS = cv2.cvtColor(frameS,cv2.COLOR_BGR2RGB)
#
#     # interface = frame
#     interface = np.zeros((800, 1500, 3), np.uint8)
#     interface[0:720,0:1280] += frame
#     interface[0:260,1280:1430] += img
#     interface[300:508, 1280:1428] += img2
#
#
#     i+=1
#     if i==15:
#
#         facesCurFrame = fr.face_locations(frameS)
#         encodesCurFrame = fr.face_encodings(frameS,facesCurFrame)
#         i=0
#
#
#
#
#     for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
#         matches = fr.compare_faces(encodeListKnown,encodeFace)
#         faceDis = fr.face_distance(encodeListKnown,encodeFace)
#
#         matchIndex = np.argmin(faceDis)
#         name = "UNKNOWN"
#         if matches[matchIndex]:
#             name = className[matchIndex]
#             print(name)
#             y1,x2,y2,x1 = faceLoc
#             print(y1,x2,y2,x1)
#             y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
#             frame = cv2.rectangle(interface,(x1,y1),(x2,y2),(0,255,0),1)
#             cv2.rectangle(interface,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
#             cv2.putText(interface,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
#             markAttend(name)
#     cv2.imshow("okno", interface)
#     cv2.waitKey(30)
#



# photo = face_recognition.load_image_file("Biometrics/photo/Video.jpeg")
# photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
# # faceLoc = face_recognition.face_locations(photo)[0]
# encode = face_recognition.face_encodings(photo)[0]
#
# result = face_recognition.compare_faces(gggg,encode)
# print(result)


































# import mysql.connector
#
# # Подключаемся к mysql
# db = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         passwd='qwerty',
#         port='3306',
#         database='visione')
#
# cursor = db.cursor()

# import datetime

# first_monday = datetime.date(2020,8,31)
# timedelta = datetime.timedelta(days=7)
# print(first_monday+timedelta)
#2






# from util import functions as f
# import datetime
#
# db, cursor = f.connect()
# # Part of Day ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# first_monday = datetime.date(2020,8,31)
# f.addPartOfDay(first_monday)






































# for x in range(3,8+1):
#     print(x)
#     print(x%2)
#
# print("lll"+str(f.returnNumberOfDay("Wednesday")))



# f.setGroupName()

# f.registerUserData()


# sql = "SELECT * FROM Groupes"
# cursor.execute(sql)
# result = cursor.fetchall()
# groupList = []
# for x in result:
#     groupList.append(x[1])
# group = f.choose(groupList)
# print(group)

# while True:
#     # reconnect - обновить таблицу(mysql)
#     db.reconnect()

# mycursor.execute("CREATE DATABASE visione")

# mycursor.execute("SHOW DATABASES")

# mycursor.execute("CREATE TABLE useress (name VARCHAR(255), surname VARCHAR(255), group VARCHAR(255), biometrics VARCHAR(255))")

# mycursor.execute("CREATE TABLE biometrics (id INT AUTO_INCREMENT PRIMARY KEY, idUser INT, pathPhoto VARCHAR(255), encode VARCHAR(255))")

# mycursor.execute("CREATE TABLE user (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), surname VARCHAR(255), groupq VARCHAR(255), biometrics VARCHAR(255), disease boolean)")

# print(db)