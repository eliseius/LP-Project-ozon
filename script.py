from datetime import datetime as dt

import json
import os
import requests

from constants import CITIES_FROM_BE, CITIES_FROM_KZ, LIMIT, STATUS_CATALOGUE, URL
from input_data import get_input_data
from output import create_table, get_color_message


def get_sales_data(date_start, date_finish, status_row):
    offset = 0
    str_dt_start = dt.strftime(date_start, '%Y-%m-%dT%H:%M:%S.%fZ')
    str_dt_finish = dt.strftime(date_finish, '%Y-%m-%dT%H:%M:%S.%fZ')

    status_send= check_status(status_row)
    report = get_report_with_all_page(str_dt_start, str_dt_finish, offset, status_send)
    report_with_filter_city = check_filter_city(report)

    return report_with_filter_city


def check_status(status):
    if status in STATUS_CATALOGUE:
        return status
    else:
        get_color_message(('Не правильно указан статус отправления. В отчете не будет учтен фильтр по статусам'), 'info')


def get_report_with_all_page(str_datetime_start, str_datetime_finish, offset, status):
    report_pagination = []
    while True:
        sales_report = get_raw_sales_data(str_datetime_start, str_datetime_finish, LIMIT, offset, status)
        if sales_report is not None:
            short_report = make_short_report(sales_report)
            report_pagination.extend(short_report)
            if sales_report['result']['has_next']:
                offset += LIMIT
            else:
                break
        else:
            return None
    return report_pagination


def get_raw_sales_data(datetime_start, datetime_finish, limit, offset, status):
    headers = {'Client-Id': os.environ['OZON_CLIENT_ID'], 'Api-Key': os.environ['OZON_API_KEY'], 'Content-Type': 'application/json'}
    params = {
        'dir': 'asc',
        'filter': {
            'since': datetime_start,
            'status': status,
            'to': datetime_finish
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
    response = requests.post(URL, headers=headers, data=params)
    if response:
        try:
            sales_report = response.json()
            return sales_report
        except ValueError:
            get_color_message(('Ошибка сформированных данных'), 'error')
            return None
    else:
        get_color_message(('Сетевая ошибка'), 'error')
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


def check_filter_city(short_report):
    if short_report is not None:
        short_report_with_filter_city = [
            item_sold 
            for item_sold in short_report
            if CITIES_FROM_KZ.union(CITIES_FROM_BE) & set(item_sold['cluster_delivery'].split())
        ]
        return short_report_with_filter_city
    else:
        return None


if __name__ == '__main__':
    if get_input_data() is not None:
        date_start, date_finish, status = get_input_data()
        report = get_sales_data(date_start, date_finish, status)
        create_table(report)
