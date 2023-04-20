from settings import *
from tools import *



app = Flask(__name__)
db = SQL_DB()
p = Parser(config['Selenium']['profile_id'])

def auto_checking():
    # функция для запуска в отдельном потоке
    while True:
        more_data = db.get_records_older_than_7_days()# данные старше 7 дней из БД (с ИД)
        for data in more_data:
            share_link = data[5] # с учетом что [0] - id
            new_data = p.collecting_company_card(share_link)# только конкретную карточку по полю map_link
            db.update_data(new_data, id=data[0])# само обновление данных
        time.sleep(3600)# в сон на час

@app.route('/parse_companies', methods=['PUT'])
def update_data():
    data = request.json
    # тут должно выполнятся приложение
    if 'search_req' in data.keys() and 'city' in data.keys():
        parsing_data:list[dict] = p.ya_map(data['search_req'],data['city'],limit = 5 )
        parsing_data = list(
            map(
            lambda d: (d.get('photos'), # для поля images
                       d.get('title'), # для поля title
                       d.get('map_link'), # для поля page_link
                       d.get('coords'), # для поля coordinates
                       d.get('share_link'), # для поля map_link
                       d.get('address'),
                       d.get('city'),
                       d.get('stars'),
                       d.get('reviews'),
                       d.get('description'),
                       d.get('working_time'),
                       d.get('socials'),
                       d.get('company_site'),
                       d.get('phone_number'),
                       d.get('tags')),parsing_data))
        for data in parsing_data:
            db.insert_data(data)
        db.test_working() # выводим то что в бд в терминал
        return jsonify({"status": "success", "message": "Data updated."})
    else:
        return jsonify({"status": "error", "message": "You are loss 'search_req' or 'city' in put your data"})


if __name__ == "__main__":
    Thread(target=auto_checking,args=()).start()
    app.run(host=config['server']['ip'], port=config['server']['port'])