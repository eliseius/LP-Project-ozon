from datetime import datetime

import json
import os
import requests


def getting_sales_data(date_start, date_finish, limit, offset, status):
    str_datetime_start = datetime.strftime(date_start, '%Y-%m-%dT%H:%M:%S.%fZ')
    str_datetime_finish = datetime.strftime(date_finish, '%Y-%m-%dT%H:%M:%S.%fZ')
    status_send = check_status(status)

    go_to_url = "https://api-seller.ozon.ru/v3/posting/fbs/list"
    headers = {'Client-Id': os.environ['OZON_CLIENT_ID'], 'Api-Key': os.environ['OZON_API_KEY'], 'Content-Type': 'application/json'}
    params = {
        'dir': 'asc',
        'filter': {
            'since': str_datetime_start,
            'status': status_send,
            'to': str_datetime_finish
        },
        'limit': limit,
        'offset': offset,
        'translit': True,
        'with': {
            'analytics_data': True,
            'financial_data': True,
        }
    }

    params = json.dumps(params)
    response = requests.post(go_to_url, headers=headers, data=params)
    if response:
        try:
            sales_report = response.json()
        except(ValueError):
            print('Ошибка сформированных данных')
            return None
    else:
        print('Сетевая ошибка')
        return None

    return make_short_report(sales_report)


def make_short_report(sales_report):
    all_item_sold = sales_report['result']['postings']
    short_report = []
    for one_item_sold in all_item_sold:
        inform_every_item_sold = {
            'posting_number': one_item_sold['posting_number'],
            'shipment_date': one_item_sold['shipment_date'],
            'price': one_item_sold['products'][0]['price'],
            'name': one_item_sold['products'][0]['name'],
            'quantity': one_item_sold['products'][0]['quantity'],
            'cluster_delivery': one_item_sold['financial_data']['cluster_to']
        }

        short_report.append(inform_every_item_sold)

    return short_report


def check_status(status):
    status_catalogue = ['awaiting_registration', 'acceptance_in_progress', 'awaiting_approve', 
                        'awaiting_packaging', 'awaiting_deliver', 'arbitration', 'client_arbitration', 
                        'delivering', 'driver_pickup', 'delivered', 'cancelled', 
                        'not_accepted', 'sent_by_seller'
                        ]

    if status in status_catalogue:
        return status
    else:
        print('Не правильно указан статус отправления. В отчете не будет учтен фильтр по статусам')
        return None