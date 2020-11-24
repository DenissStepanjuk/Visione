from util import functions

db, cursor = functions.connect()

# Создаём класс группы
class Groupes:
    # Инициализируем данные группы
    def __init__(self):
        self.groupID = 0
        self.name = "NULL"

    # Регистрируем данные группы
    def groupRegistration(self):
        self.name = input("Groupe name: ")

    # Получить ID группы автоматически присваемый базой данных
    def getGroupeID(self):
        try:
            sql = "SELECT groupID FROM Groupes WHERE name='" + self.name + "'"
            cursor.execute(sql)
            groupID = cursor.fetchall()
            self.groupID = groupID[0][0]
        except:
            print("Wrong")

    # Вводим данные группы в базу данных
    def insertGroupeIntoDatabase(self):
        # reconnect - обновить соединение с базой данных
        db.reconnect()
        cursor.execute("INSERT INTO Groupes (name) VALUES ('"+self.name+"')")
        db.commit()

    # Получить ID группы автоматически присваемый базой данных из списка всех групп
    def getGroupeIDFromList(self):
        # reconnect - обновить соединение с базой данных
        db.reconnect()
        sql = "SELECT * FROM Groupes"
        cursor.execute(sql)
        result = cursor.fetchall()
        groupList = []

        for x in result:
            groupList.append(x[1])

        group = functions.choose(groupList)
        sql = "SELECT groupID FROM Groupes WHERE name='" + group + "'"
        cursor.execute(sql)
        groupID = cursor.fetchall()
        return groupID[0][0]






Q2 = "CREATE TABLE Groupes (groupID int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50))"