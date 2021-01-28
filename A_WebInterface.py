import datetime
import numpy as np
import cv2
import face_recognition

from util import functions
from util import videoFunctions

from entities import Attendance
from entities import Notification
from entities import Biometrics

# Задаём кабинет где находиться камера
defaultClassroom = "44"

# Подключаемся к вебкамере
cap = cv2.VideoCapture(1)



# подключаемся к базе данных
db, cursor = functions.connect()


# Обьявляем массивы, где будет хранится информация о неизвестных для системы пользователях
# Добавляеи
usersUnknown = ["first"]
usersUnknownEncode = Biometrics.Biometrics().uploadEncodeByPath(["Biometrics/encode/userID_25.csv"])
usersUnknownEncodePath = []
unknownCount = 0


while True:
    db.reconnect()
    # Проверяем фотографии на сервере
    # Если они не энкодированы, то проделываем это с ними
    # и отмечаем
    # -------------------------------------------------------------------------------------
    sql = "SELECT path_photo, biometricsid FROM biometrics WHERE check_photo = 0"
    cursor.execute(sql)
    pathsPhoto = cursor.fetchall()
    # print(pathsPhoto)

    for x in pathsPhoto:
        print(x[0])


        # videoFunctions.saveEncode(x[0])
        photo = face_recognition.load_image_file("C:/Users/Automatik/Documents/IntelliJ IDEA/WebInterface/src/main/resources/static/uploadPhotos/"+x[0])
        photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
        # faceLoc = face_recognition.face_locations(photo)[0]
        encode = face_recognition.face_encodings(photo)[0]
        pathEncode = "Biometrics/encode/userID" + str(x[1]) + ".csv"
        np.savetxt(pathEncode, encode)

        sql = "UPDATE biometrics SET path_encode='"+pathEncode+"' WHERE biometricsid = '"+str(x[1])+"'"
        cursor.execute(sql)
        db.commit()


        sql2 = "UPDATE biometrics SET check_photo=1 WHERE biometricsid = '"+str(x[1])+"'"
        cursor.execute(sql2)
        db.commit()
        print(pathEncode)
    # -------------------------------------------------------------------------------------






    # Текущие дата и время
    date_now = datetime.datetime.now().date()
    time_now = datetime.datetime.now().time()
    # раскоментировать в случае теста
    date_now = datetime.date(2021, 2, 15)
    time_now = datetime.time(8,40,16)
    #
    usersAccessDenied = []
    usersAccessDeniedEcode = []
    usersAccessDeniedEcodePath = []

    usersAccessApproved = []
    usersAccessApprovedEncode = []
    usersAccessApprovedEncodePath = []
    #
    partofdayID = 0



    # Добавляем в массив usersAccessDenied ID всех пользователей из базы данных
    usersAccessDenied = []
    sql = "SELECT userID FROM Users"
    cursor.execute(sql)
    uAD = cursor.fetchall()
    for x in uAD:
        usersAccessDenied.append(x[0])



    # --------------------------------------------------------------------------------------------------------------
    # Получаем из базы данных временные промежутки в которые проводятся уроки,
    # значения возвращаются как массив элементов timedelta
    sql = "SELECT time_start, time_end FROM part_of_day WHERE date='" + str(date_now) + "'"
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
        s_t = (datetime.datetime.combine(datetime.date(1, 1, 1), time_0) + start - t_delta).time()
        e_t = (datetime.datetime.combine(datetime.date(1, 1, 1), time_0) + end).time()

        # Получаем partofdayID, запрос в базу данных по дню (сегодня), кабинету (текущему), времени окончания урока
        if s_t < time_now and e_t > time_now:
            sql = "SELECT part_of_dayID FROM part_of_day WHERE date='" + str(date_now) + "' AND classroomid_classroomid = '" + str(
                defaultClassroom) + "' AND time_end= '" + str(e_t) + "'"
            cursor.execute(sql)
            partofdayID = cursor.fetchall()
            partofdayID = partofdayID[0][0]
            print(partofdayID)
            timeLimit = e_t

    # ------------------------------------------------------------------------------------------------------------pppppppppppppppppppppppppppppppppppppppppppp

    print(partofdayID)
    # Если partofdayID != 0, значит идёт урок.
    # Следует вычеркнуть из массива usersAccessDenied ID всех пользователей
    # которые долэны быть на уроке и добавить их в массив usersAccessApproved = [].
    if partofdayID != 0:
        # Добавляем в массив usersAccessApproved ID преподователя, через запрос к базе данных, к таблице
        # PartOfDay через partofdayID

        sql = "SELECT userid_userid FROM part_of_day WHERE part_of_dayid='" + str(partofdayID) + "'"
        cursor.execute(sql)
        teacherID = cursor.fetchall()
        usersAccessApproved.append(teacherID[0][0])

        # Получаем timetableID, расписание к которому относится наша пара,
        # для каждой группы оно уникальное
        sql = "SELECT timetableid_timetableid FROM part_of_day WHERE part_of_dayid='" + str(partofdayID) + "'"
        cursor.execute(sql)
        timetableID = cursor.fetchall()
        timetableID = timetableID[0][0]

        # Получаем ID группы у которой проходит пара по timetableID
        sql = "SELECT groupid_groupid FROM timetables WHERE timetableid='" + str(timetableID) + "'"
        cursor.execute(sql)
        groupID = cursor.fetchall()
        groupID = groupID[0][0]

        # Получаем ID пользователей из этой группы
        sql = "SELECT users_userid FROM groupes_users WHERE groupes_groupid='" + str(groupID) + "'"
        cursor.execute(sql)
        userID = cursor.fetchall()

        # Додавляем ID всех пользователей в массив usersAccessApproved
        for x in userID:
            usersAccessApproved.append(x[0])
        print("usersAccessApproved" + str(usersAccessApproved))

        # Так как на данный момент в массиве usersAccessDenied буквально все пользователи системы,
        # то убираем из него ID пользователей, которые в массиве usersAccessApproved.
        # Таким образом получаем 2 массива, пользователей которым доступ открыт и противоложный.
        for x in usersAccessApproved:
            usersAccessDenied.remove(x)

        # ////////////////////////////////////////////////////////////////////////////////////////////////////////////////


    print(usersAccessApproved)
    print(usersAccessDenied)


    # Загружаем пути к файлам содержащие биометрические данные пользователя
    # из базы данных по id пользователя в массиве
    usersAccessDeniedEcodePath = Biometrics.Biometrics().getEncodePath(usersAccessDenied)
    if usersAccessApproved:
        usersAccessApprovedEncodePath = Biometrics.Biometrics().getEncodePath(usersAccessApproved)


    # Загружаем биометрические данные пользователей из файлов, путь к которым получили выше.
    usersAccessDeniedEcode = Biometrics.Biometrics().uploadEncodeByPath(usersAccessDeniedEcodePath)
    if usersAccessApproved:
        usersAccessApprovedEncode = Biometrics.Biometrics().uploadEncodeByPath(usersAccessApprovedEncodePath)






    # Считываем кадр с видеокамеры
    check, frame = cap.read()
    # Уменьшаем изображение
    # frameS = cv2.resize(frame, (0, 0), None, 0.5, 0.5)
    # Конвертируем изображение в другое цветовое пространство
    frameS = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # Получаем координаты лиц на изображении
    facesCurFrame = face_recognition.face_locations(frameS)
    # Получаем список биометрических данных с изображения
    encodesCurFrame = face_recognition.face_encodings(frameS,facesCurFrame)





# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # закрываем дверь
    sql2 = "UPDATE classroom SET door=0 WHERE classroomid = '" + defaultClassroom + "'"
    cursor.execute(sql2)
    db.commit()

    # Получается что для каждого лица в кадре имеется пара из координат этого лица
    # и биометрических данных. В цикле перебераем все подобные пары и сравниваем их с имеющимеся
    # биометрическимими данными в массивах usersAccessApprovedEncode, usersAccessDeniedEcode,
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matchesApproved = face_recognition.compare_faces(usersAccessApprovedEncode, encodeFace)
        faceDisApproved = face_recognition.face_distance(usersAccessApprovedEncode, encodeFace)

        matchIndexApproved = np.argmin(faceDisApproved)


        matchesDenied = face_recognition.compare_faces(usersAccessDeniedEcode, encodeFace)
        faceDisDenied = face_recognition.face_distance(usersAccessDeniedEcode, encodeFace)

        matchIndexDenied = np.argmin(faceDisDenied)

        print("matchIndexDenied")
        print(matchIndexDenied)




        matchesUnknown = face_recognition.compare_faces(usersUnknownEncode, encodeFace)
        faceDisUnknown = face_recognition.face_distance(usersUnknownEncode, encodeFace)

        matchIndexUnknown = np.argmin(faceDisUnknown)



        # открываем дверь
        if matchesApproved[matchIndexApproved]:
            sql2 = "UPDATE classroom SET door=1 WHERE classroomid = '"+defaultClassroom+"'"
            cursor.execute(sql2)
            db.commit()





        # ******************************************************* сюда добавить открывание двери в if дверь открыта
        # ******************************************************* в else дверь закрыта
        if matchesApproved[matchIndexApproved]:
            name = usersAccessApproved[matchIndexApproved]
            y1, x2, y2, x1 = faceLoc
            # print(y1, x2, y2, x1)
            # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, "ID: "+str(name), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

            # Отмечаем посещение
            attendance = Attendance.Attendance()
            attendance.attendanceRegistration(name, partofdayID, timeLimit)
            attendance.markAttendance()
            db.reconnect()

            # Проверяем и отмечаем опозавшего или заболевшего
            message = "Approved"
            notification = Notification.Notification()
            notification.notificationRegistration(partofdayID, message)
            notification.diseaseCheck(name, frame)
            notification.lateCheck(name, frame)

        elif matchesDenied[matchIndexDenied]:
            name = usersAccessDenied[matchIndexDenied]
            print(name)
            y1, x2, y2, x1 = faceLoc
            print(y1, x2, y2, x1)
            # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, "ID: "+str(name), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

            # Проверяем и отмечаем лишнего или заболевшего
            message = "Entry is denied"
            notification = Notification.Notification()
            notification.notificationRegistration(partofdayID, message)
            notification.diseaseCheck(name, frame)
            notification.excessCheck(name, frame)

        elif matchesUnknown[matchIndexUnknown]:
            name = usersUnknown[matchIndexUnknown]
            print(""+str(name))
            y1, x2, y2, x1 = faceLoc
            print(y1, x2, y2, x1)
            # y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 1)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (255, 0, 0), cv2.FILLED)
            cv2.putText(frame, str(name), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

            # Отмечаем неизвестного
            message = "Unknown person!"
            notification = Notification.Notification()
            notification.notificationRegistration(partofdayID, message)
            notification.unknownCheck(name, frame)
        else:
            usersUnknown.append("Unknown-"+str(unknownCount))
            usersUnknownEncode.append(encodeFace)
            unknownCount+=1






    cv2.imshow("okno", frame)
    cv2.waitKey(100)

    # usersUnknown = []
    # usersUnknownEncode = []
    # usersUnknownEncodePath = []