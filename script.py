from datetime import datetime

import constants
import json
import os
import requests

from input_data import get_input_data


def get_sales_data(date_start, date_finish, status):
    offset = 0
    report_pagination = []
    while True:
        sales_report = get_raw_sales_data(date_start, date_finish, constants.LIMIT, offset, status)
        if sales_report is not None:
            short_report = make_short_report(sales_report)
            report_pagination.extend(short_report)
            if sales_report['result']['has_next']:
                offset += constants.LIMIT
            else:
                break
        else:
            break
    
    report_with_filter_city = check_filter_city(report_pagination)
    return report_with_filter_city


def get_raw_sales_data(date_start, date_finish, limit, offset, status):
    str_datetime_start = datetime.strftime(date_start, '%Y-%m-%dT%H:%M:%S.%fZ')
    str_datetime_finish = datetime.strftime(date_finish, '%Y-%m-%dT%H:%M:%S.%fZ')
    status_send = check_status(status)

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
    response = requests.post(constants.URL, headers=headers, data=params)
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


def check_status(status):               
    if status in constants.STATUS_CATALOGUE:
        return status
    else:
        print('Не правильно указан статус отправления. В отчете не будет учтен фильтр по статусам')
        return None


def check_filter_city(short_report):
    short_report_with_filter_city = [
        item_sold 
        for item_sold in short_report
        if constants.CITIES_FROM_KZ_BE & set(item_sold['cluster_delivery'].split())
    ]

    return short_report_with_filter_city


if __name__ == '__main__':
    date_start, date_finish, status = get_input_data()
    get_sales_data(date_start, date_finish, status)
