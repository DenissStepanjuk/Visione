from util import functions

db, cursor = functions.connect()

# Создаём класс предмета (урока)
class Cls:
    # Инициализируем данные предмета
    def __init__(self):
        self.classID = 0
        self.name = "NULL"

    # Регистрируем данные предмета
    def classRegistration(self):
        self.name = input("Class name: ")

    # Вводим данные о предмете в базу данных
    def insertClassIntoDatabase(self):
        # reconnect - обновить соединение с базой данных
        db.reconnect()
        cursor.execute("INSERT INTO Class (name) VALUES ('"+self.name+"')")
        db.commit()

    # Получить ID предмета автоматически присваемый базой данных из списка всех предметов
    def getClassIDFromList(self):
        # reconnect - обновить соединение с базой данных
        db.reconnect()
        sql = "SELECT * FROM Class"
        cursor.execute(sql)
        result = cursor.fetchall()
        classList = []
        for x in result:
            classList.append(x[1])
        clas = functions.choose(classList)
        sql = "SELECT classID FROM Class WHERE name='" + clas + "'"
        cursor.execute(sql)
        ClassID = cursor.fetchall()
        return ClassID[0][0]


Q5 = "CREATE TABLE Class (classID int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50))"