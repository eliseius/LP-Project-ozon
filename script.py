from datetime import date, timedelta

import json
import os
import requests


def general_report_output(date_start, date_finish, limit, offset):
    str_date_start, str_date_finish = format_data_in_str(date_start, date_finish)
    try:
        limit_send = check_limit(limit)
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
        'offset': offset,
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


def format_data_in_str(date_start, date_finish):
    str_datetime_start = date_start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    date_finish = date_finish + timedelta(days=1)
    str_datetime_finish = date_finish.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return str_datetime_start, str_datetime_finish

def check_limit(limit):
    if limit == 0 or limit > 1000:
        print('Количество значений в ответе должно быть в диапазоне от 1 до 1000')
        return None
    else:
        return limit