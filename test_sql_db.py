from tools import *
from settings import *


if __name__ == "__main__":
    db = SQL_DB()
    print("Добавление элемента:")
    try:
        dat = ("image1", 
            "title1", 
            "page_link1", 
            "coordinates1", 
            "map_link1", 
            "address1", 
            "city1", 
            4.5, 
            "reviews1", 
            "description1", 
            "working_hours1", 
            "social_links1", 
            "website1", 
            "phone_number1", 
            "tags1")
        db.insert_data(dat)
        db.test_working()
    except:
        print("Ошибка")   

    print("Обновление данных...")
    try:
        upt_dat = ("image1", 
            "НОВОЕ НАЗВАНИЕ", 
            "page_link1", 
            "coordinates1", 
            "map_link1", 
            "address1", 
            "city1", 
            4.5, 
            "reviews1", 
            "description1", 
            "working_hours1", 
            "social_links1", 
            "website1", 
            "phone_number1", 
            "tags1",
            "time")
        db.update_data(upt_dat)
        db.test_working()
    except:
        print("Ошибка")
        
    print("Обновление данных...")
    try:
        upt_dat = ("image1", 
            "НОВОЕ НАЗВАНИЕ", 
            "page_link1", 
            "coordinates1", 
            "map_link1", 
            "address1", 
            "city1", 
            4.5, 
            "reviews1", 
            "description1", 
            "working_hours1", 
            "social_links1", 
            "website1", 
            "phone_number1", 
            "tags1",
            "time")
        db.update_data(upt_dat)
        db.test_working()
    except:
        print("Ошибка")
        
    db._del_tab()