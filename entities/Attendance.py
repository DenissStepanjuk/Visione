import datetime

from util import functions

db, cursor = functions.connect()
# time_now = datetime.time(10,11,16)
# Создаём класс посещаемость
class Attendance:
    # Инициализируем данные
    def __init__(self):
        self.attendanceID = 0
        self.userID = 0
        self.partofdayID = 0
        self.attendance = 0
        self.late = 0
        self.time = datetime.datetime.now().time()
        # self.time = time_now

    # Регистрируем данные
    def attendanceRegistration(self, userID, partofdayID, timeLimit):
        self.userID = userID
        self.partofdayID = partofdayID
        self.attendance = 1
        if self.time>timeLimit:
              self.late = 1

    # Вводим данные в базу данных
    def insertAttendanceIntoDatabase(self):
        # reconnect - обновить соединение с базой данных
        # reconnect - обновить соединение с базой данных
        db.reconnect()
        sql = "INSERT INTO attendance (userid_userid, part_of_dayid_part_of_dayid, attendance, late, time) VALUES (%s, %s, %s, %s, %s)"
        val = (self.userID, self.partofdayID, self.attendance, self.late, self.time)
        cursor.execute(sql, val)
        db.commit()
    # Отмечаем посещение, совершаем проверку, собираем в массив всех уже прешедших
    # если человека на видео нет в списке пришедших, то заносим его в базу
    def markAttendance(self):
      usersIDAttendance = []
      sql = "SELECT userid_userid FROM Attendance WHERE part_of_dayid_part_of_dayid='" + str(self.partofdayID) + "'"
      cursor.execute(sql)
      usersID = cursor.fetchall()
      for x in usersID:
            usersIDAttendance.append(x[0])
      print(usersID)
      print(self.userID)
      if self.userID not in usersIDAttendance:
            self.insertAttendanceIntoDatabase()








Q9 = "CREATE TABLE Attendance (attendanceID int PRIMARY KEY AUTO_INCREMENT, userID int," \
      "FOREIGN KEY (userID) REFERENCES Users(userID), partofdayID int," \
      "FOREIGN KEY (partofdayID) REFERENCES PartOfDay(partofdayID), attendance BOOLEAN, late BOOLEAN, time datetime)"