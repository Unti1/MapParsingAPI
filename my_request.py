import requests

url = "http://5.181.252.113:5000/parse_companies"

# Замените значения на свои данные для запроса
data = {
    "search_req": "Рестораны",
    "city": "Москва",
    "limit": "5"
}

response = requests.put(url, json=data)

if response.status_code == 200:
    print("Запрос выполнен успешно")
    print(response.json())
else:   
    print(f"Произошла ошибка: {response.status_code}")
    print(response.text)
# import json
# data = ['автор','звание','дата','текст']
# dct_data = {'author':None,'status':None,'date':None,'text':None,'company_answer':None}
# c = 0
# if len(data) == 4:
#     values = [data[0],data[1],data[2],data[3],"NULL"]
#     for key in dct_data:
#         dct_data[key] = values[c]
#         c += 1
# else:
#     values = [data[0],data[1],data[2],data[3],data[4]]
#     for key in dct_data:
#         dct_data[key] = values[c]
#         c += 1

        
# format_text = json.dumps(dct_data,ensure_ascii=False)
# print(format_text)