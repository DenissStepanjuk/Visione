import mysql.connector

# Подключаемся к mysql
db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd='qwerty',
        port='3306',
        database='visione')

cursor = db.cursor()

Q1 = "CREATE TABLE Users (userID int PRIMARY KEY AUTO_INCREMENT, " \
     "name VARCHAR(50), surname VARCHAR(50)," \
     "status ENUM('teacher','student','other'), disease BOOLEAN) "

Q2 = "CREATE TABLE Groupes (groupID int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50))"

Q3 = "CREATE TABLE Biometrics (biometricsID int PRIMARY KEY AUTO_INCREMENT, userID int, " \
     "FOREIGN KEY(userID) REFERENCES Users(userID), pathPhoto VARCHAR(250), pathEncode VARCHAR(250)) "

Q4 = "CREATE TABLE Timetables (timetableID int PRIMARY KEY AUTO_INCREMENT," \
     "groupID int, FOREIGN KEY(groupID) REFERENCES Groupes(groupID))"

Q5 = "CREATE TABLE Class (classID int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50))"

Q6 = "CREATE TABLE Classroom (classroomID int PRIMARY KEY AUTO_INCREMENT, address VARCHAR (50))"

Q7 = "CREATE TABLE PartOfDay (partofdayID int PRIMARY KEY AUTO_INCREMENT, timetableID int," \
     "FOREIGN KEY (timetableID) REFERENCES Timetables(timetableID), date date, time_start time, time_end time," \
     "parity ENUM('even','odd','no matter'), numberofweek int, " \
     "day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'), " \
     "numberoflesson int ,classID int, FOREIGN KEY (classID) REFERENCES Class(classID), userID int, " \
     "FOREIGN KEY (userID) REFERENCES Users(userID), classroomID int," \
     "FOREIGN KEY (classroomID) REFERENCES Classroom(classroomID))"

Q8 = "CREATE TABLE Notification (notificationID int PRIMARY KEY AUTO_INCREMENT, partofdayID int," \
      "FOREIGN KEY (partofdayID) REFERENCES PartOfDay(partofdayID), message VARCHAR(250), " \
      "type ENUM('disease','unknown','excess','late'), time time, pathPhoto VARCHAR(250))"

Q9 = "CREATE TABLE Attendance (attendanceID int PRIMARY KEY AUTO_INCREMENT, userID int," \
      "FOREIGN KEY (userID) REFERENCES Users(userID), partofdayID int," \
      "FOREIGN KEY (partofdayID) REFERENCES PartOfDay(partofdayID), attendance BOOLEAN, late BOOLEAN, time time)"

Q10 = "CREATE TABLE GroupesUsers (groupID int, userID int," \
      "FOREIGN KEY (userID) REFERENCES Users(userID)," \
      "FOREIGN KEY (groupID) REFERENCES Groupes(groupID))"

# # Создать таблицы базы данных автоматически
# # ___________________________________
# Q = [Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10]
# for q in Q:
#     cursor.execute(q)
# # ___________________________________

# Создать таблицы базы данных в ручную
cursor.execute(Q8)
