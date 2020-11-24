from util import functions
from entities import Groupes
from entities import GroupesUsers


db, cursor = functions.connect()
statusList = ['teacher', 'student', 'other']

# Создаём класс пользователя
class Users:
    # Инициализируем данные пользовтеля
    def __init__(self, disease = False):
        self.userID = 0
        self.name = "NULL"
        self.surname = "NULL"
        self.status = "other"
        self.disease = disease

    # Регистрируем данные пользовтеля
    def userRegistration(self):
        self.name = input("User name: ")
        self.surname = input("User surname: ")
        self.status = functions.choose(statusList)
        self.disease = int(input("Disease (0 or 1):"))

    # Получить ID пользователя автоматически присваемый базой данных
    def getUserID(self):
        try:
            # reconnect - обновить соединение с базой данных
            db.reconnect()
            sql = "SELECT userID FROM Users WHERE name='" + self.name + "' AND surname ='" + self.surname + "'"
            cursor.execute(sql)
            userID = cursor.fetchall()
            self.userID = userID[0][0]
        except:
            print("Wrong")


    # Вводим данные пользовател в базу данных
    def insertUserIntoDatabase(self):
        # reconnect - обновить соединение с базой данных
        db.reconnect()
        sql = "INSERT INTO Users (name, surname, status, disease) VALUES (%s, %s, %s, %s)"
        val = (self.name, self.surname, self.status, self.disease)
        cursor.execute(sql, val)
        db.commit()
        # Если пользователь студент, то добавляем связь между
        # пользователем и группой в которую он зачислен
        if self.status == "student":
            self.getUserID()
            print("/*/*/*/",self.userID)
            group = Groupes.Groupes()
            groupID = group.getGroupeIDFromList()
            GU = GroupesUsers.GroupesUsers(groupID, self.userID)
            GU.insertGroupeUserIntoDatabase()


    # получить id учителя
    def getTeacherIDFromList(self):
        db.reconnect()
        sql = "SELECT userID, name, surname FROM Users WHERE status='teacher'"
        cursor.execute(sql)
        result = cursor.fetchall()
        teachersIDArray = []
        i = 0
        for x in result:
            i += 1
            print(str(i) + ")" + x[1] + " " + x[2])
            teachersIDArray.append(x[0])
        choose = int(input("choose: "))
        return teachersIDArray[choose - 1]







# ggg = Users()
# ggg.userRegistration()
# ggg.insertUserIntoDatabase()


Q1 = "CREATE TABLE Users (userID int PRIMARY KEY AUTO_INCREMENT, " \
     "name VARCHAR(50), surname VARCHAR(50)," \
     "status ENUM('teacher','student','other'), disease BOOLEAN) "