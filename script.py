from datetime import timedelta

import json
import os
import requests


def general_report(date_start, date_finish, limit, offset):
    try:
        str_date_start, str_date_finish = format_data(date_start, date_finish)
        limit_send, offset_send = data_processing(limit, offset)
    except(TypeError):
        print('Ошибка обработки данных')
        return None

    go_to_url = "https://api-seller.ozon.ru/v3/posting/fbs/list"
    headers = {'Client-Id': os.environ['OZON_CLIENT_ID'], 'Api-Key': os.environ['OZON_API_KEY'], 'Content-Type': 'application/json'}
    params = {
        'dir': 'asc',
        'filter': {
            'since': str_date_start,
            'status': 'delivered',
            'to': str_date_finish
        },
        'limit': limit_send,
        'offset': offset_send,
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
            print('Ошибка сформированных данных')
            return None
    else:
        print('Сетевая ошибка')
        return None


def format_data(date_start, date_finish):
    str_datetime_start = date_start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    date_finish = date_finish + timedelta(days=1)
    str_datetime_finish = date_finish.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return str_datetime_start, str_datetime_finish

def data_processing(limit, offset):
    try:
        limit_int = abs(int(limit))
        offset_int = abs(int(offset))
    except(ValueError):
        print('Ошибка ввода данных')
        return None
    
    if limit_int == 0 or limit_int > 1000:
        print('Количество значений в ответе должно быть в диапазоне от 1 до 1000')
        return None
    else:
        return limit_int, offset_int


if __name__ == "__main__":
    main()
