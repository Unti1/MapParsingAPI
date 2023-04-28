from tools import *
from settings import *

db = SQL_DB()
data = db.test_working()

for d in data[-5:]:
    comment = d[9]
    f = comment.find("Посмотреть ответ организации")
    if f != -1: 
        print(comment)
        print(comment[f-50:f+50])
    else:
        print("Такой надписи нет")