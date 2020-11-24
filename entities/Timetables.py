from util import functions
from entities import Groupes

db, cursor = functions.connect()

# Создаём класс кабинета
class Timetables:
    # Инициализируем данные предмета
    def __init__(self):
        self.timetableID = 0
        self.groupID = 0

    # создаём расписание для группы
    def createTimetableForGroup(self, groupID):
        db.reconnect()
        groupID = groupID
        cursor.execute("INSERT INTO Timetables (groupID) VALUES ('" + str(groupID) + "')")
        db.commit()

    # получить id расписания по id группы
    def getTimetableIDbyGroupID(groupID):
        db.reconnect()
        sql = "SELECT timetableID FROM Timetables WHERE groupID='" + str(groupID) + "'"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]





Q4 = "CREATE TABLE Timetables (timetableID int PRIMARY KEY AUTO_INCREMENT," \
     "groupID int, FOREIGN KEY(groupID) REFERENCES Groupes(groupID))"