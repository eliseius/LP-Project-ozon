from datetime import datetime, timedelta
import json
import requests
import settings


def go_to_seller_ozon(date_start, date_finish):
    go_to_url = "https://api-seller.ozon.ru/v3/posting/fbs/list"
    headers = {'Client-Id': settings.CLIENT_ID, 'Api-Key': settings.USER_API, 'Content-Type': 'application/json'}
    params = {
        'dir': 'asc',
        'filter': {
            'since': date_start,
            'status': 'delivered',
            'to': date_finish
        },
        'limit': 1000,
        'offset': 0,
        'translit': True,
        'with': {
            'analytics_data': True,
            'financial_data': True
        }
    }
    try:
        params = json.dumps(params)
        result = requests.post(go_to_url, headers=headers, data=params)
        result.raise_for_status()
        sell_ozon = result.json()
        return sell_ozon
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return None


delta = timedelta(days=8)
date_start = datetime.now() - delta
date_start = date_start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
date_finish = datetime.now()
date_finish = date_finish.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


if __name__ == "__main__":
    print(go_to_seller_ozon(date_start, date_finish))
