import mysql.connector
# import datetime

# функция выбора, возвращает один элемент выбранный из массива
def choose(chooseList):
    chooseList = chooseList
    i = 0
    for x in chooseList:
        i += 1
        print(str(i) + ") " + x)
    choose = input("choose: ")
    return(chooseList[int(choose) - 1])

# Функция подключения к базе данных
def connect():
    db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd='qwerty',
            port='3306',
            database='tort')
    cursor = db.cursor()
    return db, cursor





















# def setGroupName():
#     db, cursor = connect()
#     groupName = input("Groupe name: ")
#     cursor.execute("INSERT INTO Groupes (name) VALUES ('"+groupName+"')")
#     db.commit()

# def setClassName():
#     db, cursor = connect()
#     className = input("Class name: ")
#     cursor.execute("INSERT INTO Class (name) VALUES ('"+className+"')")
#     db.commit()

# def setClassroomAddress():
#     db, cursor = connect()
#     classroomAddress = input("Classroom name: ")
#     cursor.execute("INSERT INTO Classroom (address) VALUES ('"+classroomAddress+"')")
#     db.commit()

# # получить id предмета
# def getClassID():
#     db, cursor = connect()
#     sql = "SELECT * FROM Class"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     classList = []
#     for x in result:
#         classList.append(x[1])
#     clas = choose(classList)
#     sql = "SELECT classID FROM Class WHERE name='" + clas + "'"
#     cursor.execute(sql)
#     ClassID = cursor.fetchall()
#     return ClassID[0][0]

# # получить id предмета
# def getClassroomID():
#     db, cursor = connect()
#     sql = "SELECT * FROM Classroom"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     classroomList = []
#     for x in result:
#         classroomList.append(x[1])
#     clasrooms = choose(classroomList)
#     sql = "SELECT classroomID FROM Classroom WHERE address='" + clasrooms + "'"
#     cursor.execute(sql)
#     ClassroomID = cursor.fetchall()
#     return ClassroomID[0][0]

# def getTeacherID():
#     sql = "SELECT userID, name, surname FROM Users WHERE status='teacher'"
#     db, cursor = connect()
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     teachersIDArray = []
#     i = 0
#     for x in result:
#         i += 1
#         print(str(i) + ")" + x[1] + " " + x[2])
#         teachersIDArray.append(x[0])
#     choose = int(input("choose: "))
#     return teachersIDArray[choose - 1]


# # получить id группы
# def getGroupeID():
#     db, cursor = connect()
#     sql = "SELECT * FROM Groupes"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     groupList = []
#     for x in result:
#         groupList.append(x[1])
#     group = choose(groupList)
#     sql = "SELECT groupID FROM Groupes WHERE name='" + group + "'"
#     cursor.execute(sql)
#     groupID = cursor.fetchall()
#     return groupID[0][0]

# --------------------------------------------------------------------------------------------------------------------------------------------------
# регистрируем юзера и вводим все данные
# def registerUserData():
#     db, cursor = connect()
#     statusList = ['teacher', 'student', 'other']
#     name = input("User name: ")
#     surname = input("User surname: ")
#     status = choose(statusList)
#     disease = int(input("Disease (0 or 1):"))
#
#     sql = "INSERT INTO Users (name, surname, status, disease) VALUES (%s, %s, %s, %s)"
#     val = (name, surname, status, disease)
#     cursor.execute(sql, val)
#     db.commit()
#     # если студент, то в таблу GroupesUsers добавляем связь мол
#     # такой-то студент в такой-то группе
#     if status == "student":
#         sql = "SELECT userID FROM Users WHERE name='"+name+"' AND surname ='"+surname+"'"
#         cursor.execute(sql)
#         userID = cursor.fetchall()
#         print(userID[0][0])
# # а
# #         # sql = "SELECT * FROM Groupes"
# #         # cursor.execute(sql)
# #         # result = cursor.fetchall()
# #         # groupList = []
# #         # for x in result:
# #         #     groupList.append(x[1])
# #         # group = choose(groupList)
# #         # sql = "SELECT groupID FROM Groupes WHERE name='" + group + "'"
# #         # cursor.execute(sql)
# #         # groupID = cursor.fetchall()
# #         # print(groupID[0][0])
#         groupID = getGroupeID
#         sql = "INSERT INTO GroupesUsers (groupID, userID) VALUES (%s, %s)"
#         val = (groupID, userID[0][0])
#         cursor.execute(sql, val)
#         db.commit()
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# # Присваиваем каждой группе расписание
# def createTimetableForGroups():
#     db, cursor = connect()
#     sql = "SELECT * FROM Groupes"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     groupIDList = []
#
#     for x in result:
#         groupIDList.append(x[0])
#
#     for x in groupIDList:
#         cursor.execute("INSERT INTO Timetables (groupID) VALUES ('" + str(x) + "')")
#         db.commit()


# # Вводим название дня текстом, возвращаем номер дня цифрой
# def returnNumberOfDay(day):
#     if day == "Monday":
#         return 0
#     if day == "Tuesday":
#         return 1
#     if day == "Wednesday":
#         return 2
#     if day == "Thursday":
#         return 3
#     if day == "Friday":
#         return 4
#     if day == "Saturday":
#         return 5
#     if day == "Sunday":
#         return 6


# # получить id расписания по id группы
# def getTimetableIDbyGroupID(groupID):
#     db, cursor = connect()
#     sql = "SELECT timetableID FROM Timetables WHERE groupID='"+str(groupID)+"'"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     return result[0][0]


# def addPartOfDay(first_monday):
#     db, cursor = connect()
#     times_start = [datetime.time(8, 30), datetime.time(10, 15), datetime.time(12, 30), datetime.time(14, 15)]
#     times_end = [datetime.time(10), datetime.time(11, 45), datetime.time(14), datetime.time(15, 45)]
#
#     # print(times_end[0])
#     #
#     print("Choose group:")
#     groupID = getGroupeID()
#
#     timetableID = getTimetableIDbyGroupID(groupID)
#     # print(timetableID)
#     #
#     from_week = int(input("Enter first week of period: "))
#     to_week = int(input("Enter last week of period: "))
#     #
#     # # Выбрать чётность недель
#     print("Choose parity:")
#     parityElements = ['even', 'odd', 'no matter']
#     parity = choose(parityElements)
#     #
#     # выбрать день недели
#     print("Choose day:")
#     daysElements = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     day = choose(daysElements)
#     numbe_of_day = returnNumberOfDay(day)
#     # print("///////",day,numbe_of_day)
#
#     number_of_lesson = int(input("Enter number of lesson: "))
#
#     # Выбрать премет
#     classID = getClassID()
#
#     # Выбрать кабинет
#     classroomID = getClassroomID()
#
#     # Выбрать учителя
#     teacherID = getTeacherID()
#
#     # прописываем пары для каждой недели в заданом промежутке
#     # в зависимости от четности недели
#     for x in range(from_week, to_week + 1):
#         if x % 2 == 0 and parity == "even":
#             timedelta = datetime.timedelta(days=7 * (x - 1) + numbe_of_day)
#             # print(timedelta)
#             date = first_monday + timedelta
#             # print(date)
#             sql = "INSERT INTO PartOfDay (timetableID, date, time_start, time_end, parity, numberofweek, day," \
#                   " numberoflesson, classID, userID, classroomID) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)"
#             val = (
#             timetableID, date, times_start[number_of_lesson - 1], times_end[number_of_lesson - 1], parity, x, day,
#             number_of_lesson, classID, teacherID, classroomID)
#             cursor.execute(sql, val)
#             db.commit()
#         if x % 2 == 1 and parity == "odd":
#             timedelta = datetime.timedelta(days=7 * (x - 1) + numbe_of_day)
#             # print(timedelta)
#             date = first_monday + timedelta
#             # print(date)
#             sql = "INSERT INTO PartOfDay (timetableID, date, time_start, time_end, parity, numberofweek, day," \
#                   " numberoflesson, classID, userID, classroomID) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)"
#             val = (
#             timetableID, date, times_start[number_of_lesson - 1], times_end[number_of_lesson - 1], parity, x, day,
#             number_of_lesson, classID, teacherID, classroomID)
#             cursor.execute(sql, val)
#             db.commit()
#         if parity == "no matter":
#             timedelta = datetime.timedelta(days=7 * (x - 1) + numbe_of_day)
#             # print(timedelta)
#             date = first_monday + timedelta
#             # print(date)
#             sql = "INSERT INTO PartOfDay (timetableID, date, time_start, time_end, parity, numberofweek, day," \
#                   " numberoflesson, classID, userID, classroomID) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)"
#             val = (
#             timetableID, date, times_start[number_of_lesson - 1], times_end[number_of_lesson - 1], parity, x, day,
#             number_of_lesson, classID, teacherID, classroomID)
#             cursor.execute(sql, val)
#             db.commit()
