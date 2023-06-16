from datetime import datetime

import json
import os
import requests


def getting_sales_data(date_start, date_finish, limit, offset):
    str_datetime_start = datetime.strftime(date_start, '%Y-%m-%dT%H:%M:%S.%fZ')
    str_datetime_finish = datetime.strftime(date_finish, '%Y-%m-%dT%H:%M:%S.%fZ')
    if limit == 0 or limit > 1000:
        print('Диапазон значений лимит от 1 до 1000')
        return None

    go_to_url = "https://api-seller.ozon.ru/v3/posting/fbs/list"
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
    result = requests.post(go_to_url, headers=headers, data=params)
    if result.status_code == requests.codes.ok:
        try:
            sales_report = result.json()
        except(ValueError):
            print('Ошибка сформированных данных')
            return None
    else:
        print('Сетевая ошибка')
        return None

    return abridged_report(sales_report)


def abridged_report(sales_report):
    all_item_sold = sales_report['result']['postings']
    modified_report = []
    for one_item_sold in all_item_sold:
        inform_every_item_sold = {}
        posting_number_item = one_item_sold['posting_number']
        inform_every_item_sold['posting_number'] = posting_number_item
        shipment_date_item = one_item_sold['shipment_date']
        inform_every_item_sold['shipment_date'] = shipment_date_item
        price_item = one_item_sold['products'][0]['price']
        inform_every_item_sold['price'] = price_item
        name_item = one_item_sold['products'][0]['name']
        inform_every_item_sold['name'] = name_item
        quantity_item = one_item_sold['products'][0]['quantity']
        inform_every_item_sold['quantity'] = quantity_item
        cluster_delivery = one_item_sold['financial_data']['cluster_to']
        inform_every_item_sold['cluster_delivery'] = cluster_delivery
        modified_report.append(inform_every_item_sold)
    return modified_report