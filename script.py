from datetime import datetime, timedelta
from calendar import monthrange
import json
import requests
import settings


def general_report(month, year):
    date_start, date_finish = format_data(month, year)
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
            'financial_data': True,
        }
    }

    params = json.dumps(params)
    result = requests.post(go_to_url, headers=headers, data=params)
    if result.status_code == requests.codes.ok:
        try:
            report_for_the_period = result.json()
            return report_for_the_period
        except(ValueError):
            print('Ошибка данных')
            return None
    else:
        print('Сетевая ошибка')
        return None


def format_data(year, month):
    date_start = datetime.strptime(f'{year}-{month}-1', '%Y-%m-%d')
    datetime_start = date_start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    last_numb_month = monthrange(year, month)[1]
    date_last_numb_month = datetime.strptime(f'{year}-{month}-{last_numb_month}', '%Y-%m-%d')
    date_finish = date_last_numb_month + timedelta(days=1)
    datetime_finish = date_finish.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return datetime_start, datetime_finish


if __name__ == "__main__":
    print(general_report(2023, 2))
