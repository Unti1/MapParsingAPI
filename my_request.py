import requests

url = "http://5.181.252.113:5000/parse_companies"

# Замените значения на свои данные для запроса
data = {
    "search_req": "Магазин продуктов",
    "city": "Санкт-Петербург"
}

response = requests.put(url, json=data)

if response.status_code == 200:
    print("Запрос выполнен успешно")
    print(response.json())
else:   
    print(f"Произошла ошибка: {response.status_code}")
    print(response.text)
