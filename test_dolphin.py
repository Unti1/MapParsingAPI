from tools import *
from settings import *

if __name__ == "__main__":

    p = Parser(config['Selenium']['profile_id'])
    data = {
        'search_req': "Салон красоты",
        'city': "Москва"
    }

    print(data['search_req'],data['city'])
    parsing_data:list[dict] = p.ya_map(data['search_req'],data['city'],limit=5)
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
        print(data)
        print(len(data))
    p.try_closing()