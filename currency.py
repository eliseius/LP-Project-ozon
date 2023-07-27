from datetime import datetime as dt
import time
import os
import requests

import constants
from output import get_color_message


# - Ошибка получения курса валют
# - Сетевая ошибка курса валют


def get_report_with_currency(report):
    if len(report) > 2:
        print('Идет получение курса валют ...')

    for item_sold in report:
        str_shipment_date = item_sold['shipment_date']
        date_shipment = dt.strptime(str_shipment_date, '%Y-%m-%dT%H:%M:%SZ').date()
        str_date_send = dt.strftime(date_shipment, '%Y-%m-%d')
        
        report_rates = get_exchange_rate(str_date_send)# можно получить None
        if report_rates is not None:
            usd_rate = report_rates['quotes']['USDRUB']
            calcuation_usd = round(float(item_sold['price']) / float(usd_rate), 2)
            item_sold['price'] = calcuation_usd
            item_sold['price_USD'] = item_sold.pop('price')
        else:
            report = None

    return report


def go_exchange_rates(str_date_send):
    access_key = os.environ['CURRENCY_API']
    responce = requests.get(f'{constants.URL_CURRENCY}?access_key={access_key}&date={str_date_send}')
    if responce:
        exchange_rates = responce.json()
        return exchange_rates
    else:
        get_color_message(('Ошибка получения курса валют'), 'error')
        return None
    

def get_exchange_rate(str_date_send):
    while True:
        report = go_exchange_rates(str_date_send)# можно получить None
        if report is None or report['success']:
            return report
            break
        elif report['error']['code'] == 106:
            continue
        else:
            errore = report['error']
            get_color_message(('Сетевая ошибка курса валют'), 'error')
            get_color_message(errore, 'error')
            return None
