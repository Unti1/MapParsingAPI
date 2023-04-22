from tools import *
from settings import *

if __name__ == "__main__":

    p = Parser(config['Selenium']['profile_id'])
    test_url = "https://yandex.ru/maps/org/oozor/29433003308/?ll=37.588610%2C55.779054&z=17"
    result = p.collecting_company_card(test_url)
    print(result.get('reviews'))
    p.try_closing()