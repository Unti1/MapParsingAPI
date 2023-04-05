from settings import *
from tools import *



app = Flask(__name__)
db = SQL_DB(config['SQL']['database'])
p = Parser(config['Selenium']['profile_id'])

def auto_checking():
    while True:
        more_data = db.get_records_older_than_7_days()
        for data in more_data:
            share_link = data[5]
            new_data = p.collecting_company_card(share_link)
            db.update_data(new_data)
        time.sleep(3600)

@app.route('/parse_companies', methods=['PUT'])
def update_data():
    data = request.json
    # тут должно выполнятся приложение
    if 'search_req' in data.keys() and 'city' in data.keys():
        parsing_data = p.ya_map(data['search_req'],data['city'])
        parsing_data = list(map(lambda d: (d['photos'],d['title'],d['map_link'],d['coords'],d['share_link'],d['address'],d['city'],d['stars'],d['reviews'],d['description'],d['working_time'],d['socials'],d['company_site'],d['phone_number'],d['tags']),parsing_data))
        for data in parsing_data:
            db.insert_data(parsing_data)
        return jsonify({"status": "success", "message": "Data updated."})
    else:
        return jsonify({"status": "error", "message": "You are loss 'search_req' or 'city' in put your data"})

if __name__ == "__main__":
    Thread(target=auto_checking,args=()).start()
    app.run(host=config['server']['ip'], port=config['server']['port'])
    # p.ya_map("Салоны красоты","Москва")
    # print(p.ya_company_parsing(['https://yandex.ru/maps/-/CCUWv2v6sB']))