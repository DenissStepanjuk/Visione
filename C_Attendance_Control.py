import datetime
import numpy as np
import cv2
import face_recognition

from util import functions
from entities import Attendance
from entities import Notification
from entities import Biometrics

# Задаём кабинет где находиться камера
defaultClassroom = "VK44"

# Текущие дата и время
date_now = datetime.datetime.now().date()
time_now = datetime.datetime.now().time()
# раскоментировать в случае теста
date_now = datetime.date(2020, 9, 7)
time_now = datetime.time(11,11,16)


# подключаемся к базе данных
db, cursor = functions.connect()

# Получаем из базы данных ID нашего кабинета
sql = "SELECT classroomID FROM Classroom WHERE address='" + defaultClassroom + "'"
cursor.execute(sql)
classroomID = cursor.fetchall()
classroomID = classroomID[0][0]
print(classroomID)

cap = cv2.VideoCapture(0)

usersUnknown = []
usersUnknownName = []
i=0



# Добавляем в массив usersAccessDenied ID всех пользователей из базы данных
usersAccessDenied = []
sql = "SELECT userID FROM Users"
cursor.execute(sql)
uAD = cursor.fetchall()

for x in uAD:
    usersAccessDenied.append(x[0])

usersAccessApproved = []
update = 0


while True:
# --------------------------------------------------------------------------------------------------------------
    # Получаем из базы данных временные промежутки в которые проводятся уроки,
    # значения возвращаются как массив элементов timedelta
    sql = "SELECT time_start, time_end FROM PartOfDay WHERE date='" + str(date_now) + "' AND classroomID = '"+str(classroomID)+"'"
    cursor.execute(sql)
    times = cursor.fetchall()

    # # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # time_0 время 00:00:00 необходимо чтобы из элемента timedelta
    # получть элемент времени
    time_0 = datetime.time(0)
    # t_delta элемент timedelta, который искользуется с целью указать, за сколько до начала пары
    # начать отмечать приходящих
    t_delta = datetime.timedelta(minutes=15)

    # Проходим через все временные промежутки сравнивая их с текущим временем
    # с целью выявить текущую пару
    for start, end in times:
        # Конвертируем элементы timedelta из массива в элементы времени
        s_t = (datetime.datetime.combine(datetime.date(1,1,1),time_0) + start-t_delta).time()
        e_t = (datetime.datetime.combine(datetime.date(1,1,1),time_0) + end).time()

        # Получаем partofdayID, запрос в базу данных по дню (сегодня), кабинету (текущему), времени окончания урока
        if s_t < time_now and e_t > time_now:
            sql = "SELECT partofdayID FROM PartOfDay WHERE date='" + str(date_now) + "' AND classroomID = '" + str(
                classroomID) + "' AND time_end= '"+str(e_t)+"'"
            cursor.execute(sql)
            partofdayID = cursor.fetchall()
            partofdayID = partofdayID[0][0]
            timeLimit = e_t




    # ------------------------------------------------------------------------------------------------------------pppppppppppppppppppppppppppppppppppppppppppp
            if update == 0:
                # Добавляем в массив usersAccessApproved ID преподователя, через запрос к базе данных, к таблице
                # PartOfDay через partofdayID


                sql = "SELECT userID FROM PartOfDay WHERE partofdayID='" + str(partofdayID) + "'"
                cursor.execute(sql)
                teacherID = cursor.fetchall()
                usersAccessApproved.append(teacherID[0][0])

                # Получаем timetableID, расписание к которому относится наша пара,
                # для каждой группы оно уникальное
                sql = "SELECT timetableID FROM PartOfDay WHERE partofdayID='" + str(partofdayID) + "'"
                cursor.execute(sql)
                timetableID = cursor.fetchall()
                timetableID = timetableID[0][0]

                # Получаем ID группы у которой проходит пара по timetableID
                sql = "SELECT groupID FROM Timetables WHERE timetableID='" + str(timetableID) + "'"
                cursor.execute(sql)
                groupID = cursor.fetchall()
                groupID = groupID[0][0]

                # Получаем ID пользователей из этой группы
                sql = "SELECT userID FROM GroupesUsers WHERE groupID='" + str(groupID) + "'"
                cursor.execute(sql)
                userID = cursor.fetchall()

                # Додавляем ID всех пользователей в массив usersAccessApproved
                for x in userID:
                    usersAccessApproved.append(x[0])
                print("usersAccessApproved"+ str(usersAccessApproved))

                # Так как на данный момент в массиве usersAccessDenied буквально все пользователи системы,
                # то убираем из него ID пользователей, которые в массиве usersAccessApproved.
                # Таким образом получаем 2 массива, пользователей которым доступ открыт и противоложный.
                for x in usersAccessApproved:
                    usersAccessDenied.remove(x)
                update = 1
                # ////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    # ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp


    # ---------------------------------------------------------------------------------------------------------------------++++++++++++++++++++++++++++++++++++++++++++++
    if time_now == timeLimit:
        # Добавляем в массив usersAccessDenied ID всех пользователей из базы данных
        usersAccessDenied = []
        sql = "SELECT userID FROM Users"
        cursor.execute(sql)
        uAD = cursor.fetchall()

        for x in uAD:
            usersAccessDenied.append(x[0])

        usersAccessApproved = []
        i=0
        usersUnknown = []
        usersUnknownName = []
        usersAccessDeniedEcodePath  = []
        usersAccessApprovedEncodePath  = []
        usersAccessDeniedEcode  = []
        usersAccessApprovedEncode  = []

    # Пути к файлам содержащих биометрические данные пользователя
    usersAccessDeniedEcodePath = Biometrics.Biometrics().getEncodePath(usersAccessDenied)
    if usersAccessApproved:
        usersAccessApprovedEncodePath = Biometrics.Biometrics().getEncodePath(usersAccessApproved)


    # биометрические данные пользователей
    usersAccessDeniedEcode = Biometrics.Biometrics().uploadEncodeByPath(usersAccessDeniedEcodePath)
    if usersAccessApproved:
        usersAccessApprovedEncode = Biometrics.Biometrics().uploadEncodeByPath(usersAccessApprovedEncodePath)









    check, frame = cap.read()
    # frameS = cv2.resize(frame, (0, 0), None, 0.5, 0.5)
    frameS = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(frameS)
    encodesCurFrame = face_recognition.face_encodings(frameS,facesCurFrame)



    if usersAccessApproved:
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matchesApproved = face_recognition.compare_faces(usersAccessApprovedEncode,encodeFace)
            faceDisApproved = face_recognition.face_distance(usersAccessApprovedEncode,encodeFace)

            matchIndexApproved = np.argmin(faceDisApproved)

            if matchesApproved[matchIndexApproved]:
                name = usersAccessApproved[matchIndexApproved]
                print(name)
                y1,x2,y2,x1 = faceLoc
                print(y1,x2,y2,x1)
                # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
                frame = cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),1)
                cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(frame,str(name),(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                # --------------------------------------------------------------------------------------------------------------------------------
                attendance = Attendance.Attendance()
                attendance.attendanceRegistration(name, partofdayID, timeLimit)
                attendance.markAttendance()
                db.reconnect()
                message = "Approved"
                notification = Notification.Notification()
                notification.notificationRegistration(partofdayID, message)
                notification.diseaseCheck(name,frame)
                notification.lateCheck(name,frame)
                # markAttend(name)
            elif len(matchesApproved) != len(facesCurFrame):

                # for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matchesDenied = face_recognition.compare_faces(usersAccessDeniedEcode, encodeFace)
                faceDisDenied = face_recognition.face_distance(usersAccessDeniedEcode, encodeFace)

                matchIndexDenied = np.argmin(faceDisDenied)
                if matchesDenied[matchIndexDenied]:
                    name = usersAccessDenied[matchIndexDenied]
                    print(name)
                    y1, x2, y2, x1 = faceLoc
                    print(y1, x2, y2, x1)
                    # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
                    cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, str(name), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                    message = "Denied"
                    notification = Notification.Notification()
                    notification.notificationRegistration(partofdayID, message)
                    notification.diseaseCheck(name,frame)
                    notification.excessCheck(name,frame)

                elif usersUnknown:
                    matchesUnknown = face_recognition.compare_faces(usersUnknown, encodeFace)
                    faceDisUnknown = face_recognition.face_distance(usersUnknown, encodeFace)

                    matchIndexUnknown = np.argmin(faceDisUnknown)
                    if matchesUnknown[matchIndexUnknown]:
                        name = usersUnknownName[matchIndexUnknown]
                        print(name)
                        y1, x2, y2, x1 = faceLoc
                        print(y1, x2, y2, x1)
                        # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
                        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
                        cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                        cv2.putText(frame, str(name), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                        message = "UNKNOWN"
                        notification = Notification.Notification()
                        notification.notificationRegistration(partofdayID, message)
                        notification.unknownCheck(name,frame)


                    else:
                        i+=1
                        usersUnknownName.append("UNKNOWN "+str(i))
                        usersUnknown.append(encodeFace)
                        print("unknown+")
                else:
                    i+=1
                    usersUnknownName.append("UNKNOWN "+str(i))
                    usersUnknown.append(encodeFace)


                    print("unknown/////////////////////////////////////////////////////")
    else:
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):

                # for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matchesDenied = face_recognition.compare_faces(usersAccessDeniedEcode, encodeFace)
            faceDisDenied = face_recognition.face_distance(usersAccessDeniedEcode, encodeFace)

            matchIndexDenied = np.argmin(faceDisDenied)
            if matchesDenied[matchIndexDenied]:
                    name = usersAccessDenied[matchIndexDenied]
                    print(name)
                    y1, x2, y2, x1 = faceLoc
                    print(y1, x2, y2, x1)
                    # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
                    cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, str(name), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                    # message = "Denied"
                    # notification = Notification.Notification()
                    # notification.notificationRegistration(partofdayID, message)
                    # notification.diseaseCheck(name)
                    # notification.excessCheck(name)

            elif usersUnknown:
                matchesUnknown = face_recognition.compare_faces(usersUnknown, encodeFace)
                faceDisUnknown = face_recognition.face_distance(usersUnknown, encodeFace)

                matchIndexUnknown = np.argmin(faceDisUnknown)
                if matchesUnknown[matchIndexUnknown]:
                        name = usersUnknownName[matchIndexUnknown]
                        print(name)
                        y1, x2, y2, x1 = faceLoc
                        print(y1, x2, y2, x1)
                        # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
                        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
                        cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                        cv2.putText(frame, str(name), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                        # message = "UNKNOWN"
                        # notification = Notification.Notification()
                        # notification.notificationRegistration(partofdayID, message)
                        # notification.unknownCheck(name)


                else:
                        i += 1
                        usersUnknownName.append("UNKNOWN " + str(i))
                        usersUnknown.append(encodeFace)
                        print("unknown+")
            else:
                    i += 1
                    usersUnknownName.append("UNKNOWN " + str(i))
                    usersUnknown.append(encodeFace)

                    print("unknown/////////////////////////////////////////////////////")

                    # UNKNOWN = "UNKNOWN"
                    # y1,x2,y2,x1 = faceLoc
                    # print(y1,x2,y2,x1)
                    # # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
                    # frame = cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),1)
                    # cv2.rectangle(frame,(x1,y2-35),(x2,y2),(255,0,0),cv2.FILLED)
                    # cv2.putText(frame,UNKNOWN,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
    cv2.imshow("okno", frame)
    cv2.waitKey(100)