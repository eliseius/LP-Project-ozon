from datetime import datetime as dt

import json
import os
import requests

from constants import CITIES_FROM_AM, CITIES_FROM_KG, CITIES_FROM_BE, CITIES_FROM_KZ, LIMIT, URL_OZON
from queries_in_db import get_report_with_currency
from utils import save_error_ozon


def get_sales_data(date_start, date_finish, status):
    offset = 0
    str_dt_start = dt.strftime(date_start, '%Y-%m-%dT%H:%M:%S.%fZ')
    str_dt_finish = dt.strftime(date_finish, '%Y-%m-%dT%H:%M:%S.%fZ')

    report = get_report_with_all_page(str_dt_start, str_dt_finish, offset, status)
    report_with_filter_city,  sum_post_in_city = check_filter_city(report)
    report_with_usd = get_report_with_currency(report_with_filter_city)
    return report_with_usd, sum_post_in_city


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
            break
    return report_pagination


def get_raw_sales_data(datetime_start, datetime_finish, limit, offset, status):
    headers = {'Client-Id': os.environ['OZON_CLIENT_ID'], 'Api-Key': os.environ['OZON_API_KEY'],
               'Content-Type': 'application/json'}

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
    response = requests.post(URL_OZON, headers=headers, data=params)
    if response:
        try:
            sales_report = response.json()
            return sales_report
        except ValueError:
            print('Ошибка сформированных данных')
            code = 700
    else:
        print('Сетевая ошибка')
        code = response.status_code
    save_error_ozon(code)
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
    report_am = []
    report_be = []
    report_kg = []
    report_kz = []
    sum_post_in_city = {}
    for item_sold in short_report:
        clusters = set(item_sold['cluster_delivery'].split())
        if CITIES_FROM_KZ.union(CITIES_FROM_AM, CITIES_FROM_KG, CITIES_FROM_BE) & clusters:
            if CITIES_FROM_AM & clusters:
                item_sold['cluster_delivery'] = 'Армения'
                report_am.append(item_sold)
            elif CITIES_FROM_BE& clusters:
                item_sold['cluster_delivery'] = 'Беларусь'
                report_be.append(item_sold)
            elif CITIES_FROM_KG& clusters:
                item_sold['cluster_delivery'] = 'Киргизия'
                report_kg.append(item_sold)
            elif CITIES_FROM_KZ& clusters:
                item_sold['cluster_delivery'] = 'Казахстан'
                report_kz.append(item_sold)

    report_with_filter_city = [*report_am, *report_be, *report_kg, *report_kz]

    sum_post_in_city['Армения'] = len(report_am)
    sum_post_in_city['Беларусь'] = len(report_be)
    sum_post_in_city['Киргизия'] = len(report_kg)
    sum_post_in_city['Казахстан'] = len(report_kz)

    return report_with_filter_city, sum_post_in_city
