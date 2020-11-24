from util import functions

db, cursor = functions.connect()

# Создаём класс кабинета
class Classroom:
    # Инициализируем данные предмета
    def __init__(self):
        self.classroomID = 0
        self.address = "NULL"

    # Регистрируем данные кабинета
    def classroomRegistration(self):
        self.address = input("Classroom address: ")

    # Вводим данные о кабинете в базу данных
    def insertClassroomIntoDatabase(self):
        # reconnect - обновить соединение с базой данных
        db.reconnect()
        cursor.execute("INSERT INTO Classroom (address) VALUES ('"+self.address+"')")
        db.commit()

    # Получить ID кабинета автоматически присваемый базой данных из списка всех предметов
    def getClassroomIDFromList(self):
        # reconnect - обновить соединение с базой данных
        db.reconnect()
        sql = "SELECT * FROM Classroom"
        cursor.execute(sql)
        result = cursor.fetchall()
        classroomList = []
        for x in result:
            classroomList.append(x[1])
        clasrooms = functions.choose(classroomList)
        sql = "SELECT classroomID FROM Classroom WHERE address='" + clasrooms + "'"
        cursor.execute(sql)
        ClassroomID = cursor.fetchall()
        return ClassroomID[0][0]


Q6 = "CREATE TABLE Classroom (classroomID int PRIMARY KEY AUTO_INCREMENT, address VARCHAR (50))"