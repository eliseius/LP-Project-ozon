from datetime import datetime

import json
import os
import requests


def get_sales_data(date_start, date_finish):
    limit = 1000
    offset = 0
    report_pagination = []

    while True:
        sales_report = get_global_report(date_start, date_finish, limit, offset)
        try:
            value_pagination = sales_report['result']['has_next']
        except TypeError:
            break

        if value_pagination:
            short_report = make_short_report(sales_report)
            report_pagination.extend(short_report)
            offset += limit
        else:
            short_report = make_short_report(sales_report)
            report_pagination.extend(short_report)
            break
    
    return report_pagination


def get_global_report(date_start, date_finish, limit, offset):
    str_datetime_start = datetime.strftime(date_start, '%Y-%m-%dT%H:%M:%S.%fZ')
    str_datetime_finish = datetime.strftime(date_finish, '%Y-%m-%dT%H:%M:%S.%fZ')

    url = "https://api-seller.ozon.ru/v3/posting/fbs/list"
    headers = {'Client-Id': os.environ['OZON_CLIENT_ID'], 'Api-Key': os.environ['OZON_API_KEY'], 'Content-Type': 'application/json'}
    params = {
        'dir': 'asc',
        'filter': {
            'since': str_datetime_start,
            'status': 'delivered',
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
    response = requests.post(url, headers=headers, data=params)
    if response:
        try:
            sales_report = response.json()
            return sales_report
        except ValueError:
            print('Ошибка сформированных данных')
            return None
    else:
        print('Сетевая ошибка')
        return None


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