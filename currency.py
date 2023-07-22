from datetime import datetime as dt
from datetime import timedelta as td
from dateutil.parser import parse
import time
import json
import os
import requests

import constants

def get_report_with_currency(report):
    # for item_sold in report:
    #     str_shipment_date = item_sold['shipment_date']
    #     date_shipment = dt.strptime(str_shipment_date, '%Y-%m-%dT%H:%M:%SZ').date()
    #     str_date_send = dt.strftime(date_shipment, '%Y-%m-%d')

    usd_rate = get_exchange_rates(str_date_send)
    calcuation_usd = round(float(item_sold['price']) / float(usd_rate), 2)
    item_sold['price'] = calcuation_usd
    item_sold['price_USD'] = item_sold.pop('price')

    time.sleep(1)

    return report


def get_exchange_rates(str_date_send):
    access_key = os.environ['CURRENCY_API']
    responce = requests.get(f'{constants.URL_CURRENCY}?access_key={access_key}&date={str_date_send}')
    if responce:
        try:
            exchange_rates = responce.json()
        except ValueError:
            print('Сетевая ошибка')
            return None
    # print(exchange_rates)
    # value_usd = exchange_rates['quotes']['USDRUB']
    return exchange_rates


def get_usd_rates(date_start, date_end):
    while True:
        date_send = date_start + td(days=1)
        print(date_send)
        if date_send > date_end:
            break
        
        str_date_send = dt.strftime(date_send, '%Y-%m-%d')# передавать строку в фомате только датаа
        report = get_exchange_rates(date_send)
        short_report = make_short_report(report)

        return short_report


def make_short_report(report):
    short_report = {
        'date': report['date'],
        'currency': report['source'],
        'value': report['quotes']['USDRUB'],
    }

    return short_report


def write_usd_rate(date_start, date_end):
    report = get_usd_rates(date_start, date_end)
    with open('exchange_rate_usd.json', 'a', encoding='utf-8') as my_file:
        json.dump(report, my_file, ensure_ascii=False, indent=4)


if __name__ ==  '__main__':
    date_start = parse('19/3/2023', dayfirst=True)
    date_end = parse('22/3/2023', dayfirst=True)

    write_usd_rate(date_start, date_end)