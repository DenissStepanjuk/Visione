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
        self.checkss = 0


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
            self.type = 0
            self.pathPhoto = "images/Disease/"+str(self.type)+" - "+str(self.partofdayID)+" - "+str(userID)+".jpeg"
            self.markNotification(frame)


    # Выводим уведомление о не зарегестрированом человеке в системе
    def unknownCheck(self, userID, frame):
        self.type = 1
        self.pathPhoto = "images/Unknown/"+str(self.type)+" - "+str(self.partofdayID)+" - "+str(userID)+".jpeg"
        self.markNotification(frame)

    # Выводим уведомление о  человеке, который не должен находиться в кабинете
    def excessCheck(self, userID, frame):
        self.type = 2
        self.pathPhoto = "images/Excess/"+str(self.type)+" - "+str(self.partofdayID)+" - "+str(userID)+".jpeg"
        self.markNotification(frame)

    # Выводим уведомление о опоздавшем человеке
    def lateCheck(self, userID, frame):
        sql = "SELECT late FROM Attendance WHERE userid_userid ='" + str(userID) + "' AND part_of_dayid_part_of_dayid = '"+str(self.partofdayID)+"'"
        cursor.execute(sql)
        late = cursor.fetchall()
        # print(late)
        # late = late[0][0]
        print(str(late) + "late++++++++++" + str(userID) + str(self.partofdayID))
        if late == [(1,)]:

            print(str(late)+"late///////////"+str(userID)+str(self.partofdayID))
            self.type = 3
            self.pathPhoto = "images/Late/"+str(self.type)+" - "+str(self.partofdayID)+" - "+str(userID)+".jpeg"
            self.markNotification(frame)

    # Вводим данные в базу данных
    def insertNotificationIntoDatabase(self):
        # reconnect - обновить соединение с базой данных
        db.reconnect()
        sql = "INSERT INTO notifications_datas (part_of_dayid_part_of_dayid, messagess, typess, time, path_photo, checkss) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (self.partofdayID, self.message, self.type, self.time, self.pathPhoto,self.checkss)
        cursor.execute(sql, val)
        db.commit()
    # Отмечаем посещение, совершаем проверку, собираем в массив всех уже прешедших
    # если человека на видео нет в списке пришедших, то заносим его в базу

    def markNotification(self, frame):
      pathNotificationPhoto = []
      sql = "SELECT path_photo FROM notifications_datas WHERE part_of_dayid_part_of_dayid='" + str(self.partofdayID) + "'"
      cursor.execute(sql)
      pathPhotos = cursor.fetchall()
      for x in pathPhotos:
            pathNotificationPhoto.append(x[0])
      print(pathPhotos)
      print(self.time)
      if self.pathPhoto not in pathNotificationPhoto:
            self.insertNotificationIntoDatabase()
            cv2.imwrite("C:/Users/Automatik/Documents/IntelliJ IDEA/WebInterface/src/main/resources/static/"+self.pathPhoto, frame)
            print("gotovo")
            print("C:/Users/Automatik/Documents/IntelliJ IDEA/WebInterface/src/main/resources/static/"+self.pathPhoto)









Q8 = "CREATE TABLE Notification (notificationID int PRIMARY KEY AUTO_INCREMENT, partofdayID int," \
      "FOREIGN KEY (partofdayID) REFERENCES PartOfDay(partofdayID), message VARCHAR(250), " \
      "type ENUM('disease','unknown','excess','late'), time datetime, pathPhoto VARCHAR(250))"