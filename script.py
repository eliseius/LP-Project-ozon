import json
import requests
import settings

def go_to_seller_ozon():
    go_to_url = "https://api-seller.ozon.ru/v3/posting/fbs/list"
    headers = {'Client-Id': settings.CLIENT_ID, 'Api-Key': settings.USER_API, 'Content-Type': 'application/json'}
    params = {
        'dir': 'asc',
        'filter': {
            'since': '2023-05-01T00:00:00.000Z',
            'status': 'delivered',
            'to': '2023-05-08T00:00:00.000Z'
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
        return False
    return False


if __name__ == "__main__":
    print(go_to_seller_ozon())