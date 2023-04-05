import sqlite3

class SQL_DB:
    """При создании экземпляра произойдет автоматичская авторизация с прописаной в аргументе базой данных 
    и создастся таблица companies
    """
    def __init__(self, db_name:str):
        """
        Args:
            db_name (str): Название базы данных
        """
        self.db_name = db_name
        self.connect_and_create_table()

    def connect_and_create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS companies (
                            id INTEGER PRIMARY KEY,
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
        conn.commit()
        conn.close()

    def check_duplicate_data(self, data):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM companies WHERE title=? AND page_link=? AND adress=?", (data[1], data[2], data[6]))
        duplicate_data = cursor.fetchone()

        conn.close()

        if duplicate_data:
            return True
        return False
    
    def get_records_older_than_7_days(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM companies")
        all_records = cursor.fetchall()

        old_records = []

        for record in all_records:
            record_date = datetime.strptime(record[-1], '%Y-%m-%d %H:%M:%S')
            difference = datetime.now() - record_date
            if difference.days > 7:
                old_records.append(record)

        conn.close()
        return old_records
    
    def insert_data(self, data):
        if not self.check_duplicate_data(data):# проверка на дубликат
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''INSERT INTO companies (
                                images, title, page_link, coordinates, map_link, address,
                                city, stars, reviews, description, working_hours, social_links,
                                website, phone_number, tags, parsing_time
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data + (current_time,))

            conn.commit()
            conn.close()

    def update_data(self, data):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM companies WHERE page_link=?", (data[5],))
        record_id = cursor.fetchone()

        if record_id is not None:
            data_with_id = data + (record_id[0],)
            cursor.execute('''UPDATE companies SET
                                images=?, title=?, page_link=?, coordinates=?, map_link=?, address=?,
                                city=?, stars=?, reviews=?, description=?, working_hours=?, social_links=?,
                                website=?, phone_number=?, tags=?
                            WHERE id=?''', data_with_id)

            conn.commit()
        # else:
            # print("Record not found. Can't update.")

    def delete_data(self, id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM companies WHERE id=?", (id,))

        conn.commit()
        conn.close()

    def get_all_data(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM companies")
        data = cursor.fetchall()

        conn.close()
        return data