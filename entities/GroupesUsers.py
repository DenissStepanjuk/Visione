from util import functions

db, cursor = functions.connect()

# Создаём класс свзя между группой и пользователем (студентом)
class GroupesUsers:
    # Инициализируем и регистрируем данные
    def __init__(self, groupID, userID):
        self.groupID = groupID
        self.userID = userID


    # Вводим данные пользовател в базу данных
    def insertGroupeUserIntoDatabase(self):
        # reconnect - обновить соединение с базой данных
        db.reconnect()
        sql = "INSERT INTO GroupesUsers (groupID, userID) VALUES (%s, %s)"
        val = (self.groupID, self.userID)
        cursor.execute(sql, val)
        db.commit()



Q10 = "CREATE TABLE GroupesUsers (groupID int, userID int," \
      "FOREIGN KEY (userID) REFERENCES Users(userID)," \
      "FOREIGN KEY (groupID) REFERENCES Groupes(groupID))"