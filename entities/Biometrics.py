from util import functions
from util import videoFunctions
import numpy as np


db, cursor = functions.connect()

# Создаём класс биометрия
class Biometrics:
    # Инициализируем данные биометрия
    def __init__(self):
        self.biometricsID = 0
        self.userID = 0
        self.pathPhoto = "NULL"
        self.pathEncode = "NULL"

    # Регистрируем данные биометрия
    def biometricsRegistration(self, userID):
        self.userID = userID
        photoName = "userID_"+ str(userID)
        videoFunctions.takePicture(photoName)
        self.pathPhoto = "Biometrics/photo/"+photoName+".jpeg"
        videoFunctions.saveEncode(photoName)
        self.pathEncode = "Biometrics/encode/"+photoName+".csv"

        db.reconnect()
        sql = "INSERT INTO Biometrics (userID, pathPhoto, pathEncode) VALUES (%s, %s, %s)"
        val = (self.userID, self.pathPhoto, self.pathEncode)
        cursor.execute(sql, val)
        db.commit()

# Функция на входе принимает массив ID пользователей, возвращает массив путей
# к файлам содержащих биометрические данные пользователя
    def getEncodePath(self, users):
        EcodePath = []
        for x in users:
            sql = "SELECT pathEncode FROM Biometrics WHERE userID = '" + str(x) + "'"
            cursor.execute(sql)
            path = cursor.fetchall()
            EcodePath.append(path[0][0])
        return EcodePath

    # Функция на входе принимает массив путей к файлам содержащих биометрические данные пользователей,
    # возвращаеи массив биометрических данных пользователей,
    def uploadEncodeByPath(self ,pathArray):
        encodeList = []
        for x in pathArray:
            # print(x)
            encodeList.append(np.loadtxt(x))
        return encodeList

Q3 = "CREATE TABLE Biometrics (biometricsID int PRIMARY KEY AUTO_INCREMENT, userID int, " \
     "FOREIGN KEY(userID) REFERENCES Users(userID), pathPhoto VARCHAR(250), pathEncode VARCHAR(250)) "