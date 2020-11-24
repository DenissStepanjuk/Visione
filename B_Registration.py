import datetime

from entities import Classroom
from entities import Cls
from entities import Groupes
from entities import Users
from entities import Biometrics
from entities import Timetables
from entities import PartOfDay

first_monday = datetime.date(2020,8,31)

while True:
    print("1) add class")
    print("2) add classroom")
    print("3) add group")
    print("4) add user")
    print("5) add part of day")

    choose = int(input("choose: "))

    if choose == 1:
        cls = Cls.Cls()
        cls.classRegistration()
        cls.insertClassIntoDatabase()
    elif choose == 2:
        classroom = Classroom.Classroom()
        classroom.classroomRegistration()
        classroom.insertClassroomIntoDatabase()
    elif choose == 3:
        group = Groupes.Groupes()
        group.groupRegistration()
        group.insertGroupeIntoDatabase()
        group.getGroupeID()
        timetable = Timetables.Timetables()
        timetable.createTimetableForGroup(group.groupID)
    elif choose == 4:
        user = Users.Users()
        user.userRegistration()
        user.insertUserIntoDatabase()
        user.getUserID()
        bio = Biometrics.Biometrics()
        bio.biometricsRegistration(user.userID)
    elif choose == 5:
        part_of_day = PartOfDay.PartOfDay()
        part_of_day.partOfDayRegistration()
        part_of_day.insertPartOfDayIntoDatabase(first_monday)

    else: break