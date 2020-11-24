import datetime
import cv2

from util import functions

db, cursor = functions.connect()

# Создаём класс уведомлений
class Notification:
    # Инициализируем данные
    def __init__(self):
        self.notificationID = 0
        self.partofdayID = 0
        self.message = "NULL"
        self.type = "NULL"
        self.time = datetime.datetime.now().time()
        self.pathPhoto = "NULL"


    # Регистрируем данные для уведомления
    def notificationRegistration(self, partofdayID, message):
        self.partofdayID = partofdayID
        self.message = message

    # Проверяем заболевший человек или нет
    def diseaseCheck(self, userID, frame):
        sql = "SELECT disease FROM Users WHERE userID ='" + str(userID) + "'"
        cursor.execute(sql)
        disease = cursor.fetchall()
        disease = disease[0][0]
        if disease:
            self.type = 'disease'
            self.pathPhoto = "Notification/Disease/"+str(self.type)+" - "+str(self.partofdayID)+" - "+str(userID)
            self.markNotification(frame)


    # Выводим уведомление о не зарегестрированом человеке в системе
    def unknownCheck(self, userID, frame):
        self.type = 'unknown'
        self.pathPhoto = "Notification/Unknown/"+str(self.type)+" - "+str(self.partofdayID)+" - "+str(userID)
        self.markNotification(frame)

    # Выводим уведомление о  человеке, который не должен находиться в кабинете
    def excessCheck(self, userID, frame):
        self.type = 'excess'
        self.pathPhoto = "Notification/Excess/"+str(self.type)+" - "+str(self.partofdayID)+" - "+str(userID)
        self.markNotification(frame)

    # Выводим уведомление о опоздавшем человеке
    def lateCheck(self, userID, frame):
        sql = "SELECT late FROM Attendance WHERE userID ='" + str(userID) + "' AND partofdayID = '"+str(self.partofdayID)+"'"
        cursor.execute(sql)
        late = cursor.fetchall()
        # print(late)
        # late = late[0][0]
        print(str(late) + "late++++++++++" + str(userID) + str(self.partofdayID))
        if late == [(1,)]:

            print(str(late)+"late///////////"+str(userID)+str(self.partofdayID))
            self.type = 'late'
            self.pathPhoto = "Notification/Late/"+str(self.type)+" - "+str(self.partofdayID)+" - "+str(userID)
            self.markNotification(frame)

    # Вводим данные в базу данных
    def insertNotificationIntoDatabase(self):
        # reconnect - обновить соединение с базой данных
        db.reconnect()
        sql = "INSERT INTO Notification (partofdayID, message, type, time, pathPhoto) VALUES (%s, %s, %s, %s, %s)"
        val = (self.partofdayID, self.message, self.type, self.time, self.pathPhoto)
        cursor.execute(sql, val)
        db.commit()
    # Отмечаем посещение, совершаем проверку, собираем в массив всех уже прешедших
    # если человека на видео нет в списке пришедших, то заносим его в базу

    def markNotification(self, frame):
      pathNotificationPhoto = []
      sql = "SELECT pathPhoto FROM Notification WHERE partofdayID='" + str(self.partofdayID) + "'"
      cursor.execute(sql)
      pathPhotos = cursor.fetchall()
      for x in pathPhotos:
            pathNotificationPhoto.append(x[0])
      print(pathPhotos)
      print(self.time)
      if self.pathPhoto not in pathNotificationPhoto:
            self.insertNotificationIntoDatabase()
            cv2.imwrite(self.pathPhoto+".jpeg", frame)









Q8 = "CREATE TABLE Notification (notificationID int PRIMARY KEY AUTO_INCREMENT, partofdayID int," \
      "FOREIGN KEY (partofdayID) REFERENCES PartOfDay(partofdayID), message VARCHAR(250), " \
      "type ENUM('disease','unknown','excess','late'), time datetime, pathPhoto VARCHAR(250))"