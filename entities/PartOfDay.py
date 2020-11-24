import datetime
from util import functions
from entities import Groupes
from entities import Timetables
from entities import Cls
from entities import Classroom
from entities import Users


db, cursor = functions.connect()
daysElements = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
parityElements = ['even', 'odd', 'no matter']
times_start = [datetime.time(8, 30), datetime.time(10, 15), datetime.time(12, 30), datetime.time(14, 15)]
times_end = [datetime.time(10), datetime.time(11, 45), datetime.time(14), datetime.time(15, 45)]

# Создаём класс пользователя
class PartOfDay:
    # Инициализируем данные части от дня
    def __init__(self, disease = False):
        self.partofdayID = 0
        self.timetableID = 0
        self.date = datetime.date(2020,8,31)
        self.time_start = datetime.time(0, 0)
        self.time_end = datetime.time(0, 0)
        self.parity = "no matter"
        self.numberofweek = 0
        self.day = "Monday"
        self.numberoflesson = 0
        self.classID = 0
        self.userID = 0
        self.classroomID = 0


    # Регистрируем данные части от дня
    def partOfDayRegistration(self):
        print("Choose group:")
        groupID = Groupes.Groupes().getGroupeIDFromList()
        self.timetableID = Timetables.Timetables.getTimetableIDbyGroupID(groupID)

        # Выбрать чётность недель
        print("Choose parity:")
        self.parity = functions.choose(parityElements)
        # self.numberofweek = 0
        # self.date = datetime.date(2020,8,31)
        # выбрать день недели
        print("Choose day:")
        self.day = functions.choose(daysElements)


        self.numberoflesson = int(input("Enter number of lesson: "))
        self.time_start = times_start[self.numberoflesson - 1]
        self.time_end = times_end[self.numberoflesson - 1]
        self.classID = Cls.Cls().getClassIDFromList()
        self.userID = Users.Users().getTeacherIDFromList()
        self.classroomID = Classroom.Classroom().getClassroomIDFromList()


    def insertPartOfDayIntoDatabase(self, first_monday):
        from_week = int(input("Enter first week of period: "))
        to_week = int(input("Enter last week of period: "))
        number_of_day = PartOfDay().returnNumberOfDay(self.day)
        for x in range(from_week, to_week + 1):
            if x % 2 == 0 and self.parity == "even":
                timedelta = datetime.timedelta(days=7 * (x - 1) + number_of_day)
                # print(timedelta)
                date = first_monday + timedelta
                # print(date)
                sql = "INSERT INTO PartOfDay (timetableID, date, time_start, time_end, parity, numberofweek, day," \
                      " numberoflesson, classID, userID, classroomID) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)"
                val = (self.timetableID, date, self.time_start, self.time_end, self.parity, x,
                    self.day, self.numberoflesson, self.classID, self.userID, self.classroomID)
                cursor.execute(sql, val)
                db.commit()
            if x % 2 == 1 and self.parity == "odd":
                timedelta = datetime.timedelta(days=7 * (x - 1) + number_of_day)
                # print(timedelta)
                date = first_monday + timedelta
                # print(date)
                sql = "INSERT INTO PartOfDay (timetableID, date, time_start, time_end, parity, numberofweek, day," \
                      " numberoflesson, classID, userID, classroomID) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)"
                val = (self.timetableID, date, self.time_start, self.time_end, self.parity, x,
                    self.day, self.numberoflesson, self.classID, self.userID, self.classroomID)
                cursor.execute(sql, val)
                db.commit()
            if self.parity == "no matter":
                timedelta = datetime.timedelta(days=7 * (x - 1) + number_of_day)
                # print(timedelta)
                date = first_monday + timedelta
                # print(date)
                sql = "INSERT INTO PartOfDay (timetableID, date, time_start, time_end, parity, numberofweek, day," \
                      " numberoflesson, classID, userID, classroomID) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)"
                val = (self.timetableID, date, self.time_start, self.time_end, self.parity, x,
                    self.day, self.numberoflesson, self.classID, self.userID, self.classroomID)
                cursor.execute(sql, val)
                db.commit()

    # Вводим название дня текстом, возвращаем номер дня цифрой
    def returnNumberOfDay(self, day):
        if day == "Monday":
            return 0
        if day == "Tuesday":
            return 1
        if day == "Wednesday":
            return 2
        if day == "Thursday":
            return 3
        if day == "Friday":
            return 4
        if day == "Saturday":
            return 5
        if day == "Sunday":
            return 6





Q7 = "CREATE TABLE PartOfDay (partofdayID int PRIMARY KEY AUTO_INCREMENT, timetableID int," \
     "FOREIGN KEY (timetableID) REFERENCES Timetables(timetableID), date date, time_start time, time_end time," \
     "parity ENUM('even','odd','no matter'), numberofweek int, " \
     "day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'), " \
     "numberoflesson int ,classID int, FOREIGN KEY (classID) REFERENCES Class(classID), userID int, " \
     "FOREIGN KEY (userID) REFERENCES Users(userID), classroomID int," \
     "FOREIGN KEY (classroomID) REFERENCES Classroom(classroomID))"