from datetime import datetime as dt
import time
import json
import os
import requests

import constants

def get_report_with_currency(report):
    for item_sold in report:
        str_shipment_date = item_sold['shipment_date']
        date_shipment = dt.strptime(str_shipment_date, '%Y-%m-%dT%H:%M:%SZ').date()
        str_date_send = dt.strftime(date_shipment, '%Y-%m-%d')

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
    print(exchange_rates)
    value_usd = exchange_rates['quotes']['USDRUB']
    return value_usd
