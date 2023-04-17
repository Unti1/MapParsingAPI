import mysql.connector
import datetime
def connect_to_mysql(host, user, password, database, port='3306'):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        print("Connected to MySQL")
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_table(connection):
    cursor = connection.cursor()

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
    connection.commit()
def del_tab():
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS companies")
    connection.commit()

def insert_data(connection, data_list):
    cursor = connection.cursor()

    for data in data_list:
        data = list(data)
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data.append(current_time)
        cursor.execute('''INSERT INTO companies (
                            images, title, page_link, coordinates, map_link, address,
                            city, stars, reviews, description, working_hours, social_links,
                            website, phone_number, tags, parsing_time
                          ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', data)
    connection.commit()

# Замените значения переменных на свои данные для подключения к MySQL
host = "5.181.255.14"
user = "map_parser"
password = "WxPpMADH"
database = "map_parser"

connection = connect_to_mysql(host, user, password, database)

if connection:
    del_tab()
    create_table(connection)

    data_list = [
        # Пример данных для добавления в таблицу
        ("image1", "title1", "page_link1", "coordinates1", "map_link1", "address1", "city1", 4.5, "reviews1", "description1", "working_hours1", "social_links1", "website1", "phone_number1", "tags1"),
        ("image2", "title2", "page_link2", "coordinates2", "map_link2", "address2", "city2", 3.5, "reviews2", "description2", "working_hours2", "social_links2", "website2", "phone_number2", "tags2")
    ]
    insert_data(connection, data_list)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM companies")
    data = cursor.fetchall()
    print(data)
# print(list(map(lambda x: len(x),data_list)))
    connection.close()