# Pip install requests, pip install openpyxl, pip install pandas. Скачиваем все эти библотеки
import requests
import json
import pandas as pd
from datetime import datetime

cats = [2040, 2043, 5830]


def get_json(params, cat_id):
    """получаем json с данными по заданным запросам"""
    url = f"https://lalafo.kg/api/search/v3/feed/search?&expand=url&per-page=16&category_id={cat_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
        "Accept": "application/json, text/plain, */*",
        "device": "pc"
    }
    response = requests.get(url, headers=headers)
    return response.json()


def save_json(data):
    """сохрание ответа в файл для наглядного просмотра"""
    with open('lalafo_data.json', 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        print(f'Данные сохранены в lalafo_data.json')


def get_data_from_json(json_file):
    domen_photo = 'https://img5.lalafo.com/i/posters/api'
    domen = 'https://lalafo.kg'
    result = []
    for d in json_file['items']:
        title = d['title']
        phone = d['mobile']
        description = d['description']
        cat_id = d['id']
        price = d['price']
        city = d['city']
        try:
            image = domen_photo + d['image']
        except TypeError:
            image = 'без изображения'
        try:
            nameseller = d['user']['username']
        except:
            nameseller = ''

        result.append({
            'title': title,
            'phone': phone,
            'price': price,
            'description': description,
            'image': image,
            'city': city,
            'userseller': nameseller,
            'cat_id': cat_id
        })
    return result


def save_excel(data):
    # сохранение результата в excel файл
    df = pd.DataFrame(data)
    writer = pd.ExcelWriter('lalafo_result.xlsx')
    df.to_excel(writer, 'data')
    writer.save()
    print('Все сохранено в lalafo_result.xlsx')


if __name__ == '__main__':
    params = {
        'city_id': 103184,
        'cat_id': 'cat_id',
        'price[from]': 10000,
        'price[to]': 30000,
        'currency': 'KGS',
        'per-page': 500,
        'page': 1
    }
    results = []
    for cat_id in cats:
        data_json = get_json(params, cat_id=cat_id)
        result = get_data_from_json(data_json)
        results.extend(result)
        save_excel(results)

    print(len(data_json['items']))
