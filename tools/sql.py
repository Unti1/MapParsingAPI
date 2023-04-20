from settings.config import *
import mysql.connector
import datetime

class SQL_DB:
    """При создании экземпляра произойдет автоматичская авторизация с прописаной в аргументе базой данных 
    и создастся таблица companies
    """
    def __init__(self):
        """
        Args:
            db_name (str): названние базы данных
            host (str): хост БД
            user (str): логин для БД
            password (str): пароль для БД
        """
        self.connection = self.connect_to_mysql()
        self.create_table_if_not_exists()

    def connect_to_mysql(self):
        try:
            connection = mysql.connector.connect(
                host=config['SQL']['host'],
                user=config['SQL']['user'],
                password=config['SQL']['password'],
                database=config['SQL']['database'],
            )
            print("Connected to MySQL")
            return connection
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            logging.error(traceback.format_exc())
            return None
        
    def close_connection(self):
        self.connection.close()

    def create_table_if_not_exists(self):
        
        cursor = self.connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS companies (
                            id INTEGER AUTO_INCREMENT PRIMARY KEY,
                            images TEXT,
                            title TEXT,
                            page_link TEXT,
                            coordinates TEXT,
                            map_link TEXT,
                            address TEXT,
                            city TEXT,
                            stars REAL,
                            reviews TEXT,
                            description TEXT,
                            working_hours TEXT,
                            social_links TEXT,
                            website TEXT,
                            phone_number TEXT,
                            tags TEXT,
                            parsing_time TEXT
                          )''')
        self.connection.commit()

    def check_duplicate_data(self, data):
        cursor = self.connection.cursor()
        new_d = [data[1], data[2], data[5]]
        cursor.execute("SELECT * FROM companies WHERE title=%s AND page_link=%s AND address=%s", new_d)
        duplicate_data = cursor.fetchone()
        if duplicate_data:
            print("Найден дубль, данные пропускаются")
            return True
        return False
    
    def _del_tab(self):
        cursor = self.connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS companies")
        self.connection.commit()

    def get_records_older_than_7_days(self):
        """Выдает поля из БД у который последний параметр превышает 7 дней
        По отсчету индекса делать отсчет с учетом что первое значение это id
        Returns:
            old_records[list[tuple]] : 
        """
        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM companies")
        all_records = cursor.fetchall()

        old_records = []

        for record in all_records:
            record_date = datetime.datetime.strptime(record[-1], '%Y-%m-%d %H:%M:%S')
            difference = datetime.datetime.now() - record_date
            if difference.days > 7:
                old_records.append(record)

        return old_records
    
    def insert_data(self, data):
        if not self.check_duplicate_data(data):# проверка на дубликат

            cursor = self.connection.cursor()
            data = list(data)
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data.append(current_time)
            cursor.execute('''INSERT INTO companies (
                            images, title, page_link, coordinates, map_link, address,
                            city, stars, reviews, description, working_hours, social_links,
                            website, phone_number, tags, parsing_time
                          ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', data)
            print("Данные добавлены")
            self.connection.commit()

    def update_data(self, data,id:int = None):
        cursor = self.connection.cursor()
        data = list(data)
        if id == None:
            cursor.execute("SELECT id FROM companies WHERE map_link=%s", [data[4]])
            record_id = cursor.fetchone()
        else:
            record_id = [id]
        if record_id is not None:
            print(f"До изменений: {data}")
            data[-1] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # заменяем графу времени
            data.append(record_id[0])# добавляем в конец, т.к. в следующей инструкции последнее значение sql-запроса - id 
            cursor.execute('''UPDATE companies SET
                                images=%s, title=%s, page_link=%s, coordinates=%s, map_link=%s, address=%s,
                                city=%s, stars=%s, reviews=%s, description=%s, working_hours=%s, social_links=%s,
                                website=%s, phone_number=%s, tags=%s, parsing_time=%s
                            WHERE id=%s''', data)
            self.connection.commit()
        else:
            print("Данные не найдено. Обновление не произошло.")

    def test_working(self):
        if self.connection:
            # Здесь можно выполнять операции с базой данных, например:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            for table_name in cursor:
                print(table_name)
            
            cursor.execute("SELECT * FROM companies")
            data = cursor.fetchall()
            print(data)
        
    def delete_data(self, id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM companies WHERE id=?", (id,))
        self.connection.commit()

    def get_all_data(self):
        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM companies")
        data = cursor.fetchall()
        return data