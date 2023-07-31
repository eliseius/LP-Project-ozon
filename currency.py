import logging
import os
import requests
import time

from datetime import datetime as dt

from constants import URL_CURRENCY, CURRENCY
from output import get_color_message
from utils import save_error_currency


def get_report_with_currency(report):
    for item_sold in report:
        str_shipment_date = item_sold['shipment_date']
        date_shipment = dt.strptime(str_shipment_date, '%Y-%m-%dT%H:%M:%SZ').date()
        str_date_send = dt.strftime(date_shipment, '%Y-%m-%d')
        report_rates = get_exchange_rate(str_date_send)

        if report_rates is not None:
            usd_rate = report_rates['quotes']['USDRUB']
            calcuation_usd = round(float(item_sold['price']) / float(usd_rate), 2)
            item_sold['price'] = calcuation_usd
            item_sold['price_USD'] = item_sold.pop('price')
        else:
            report = []
    return report


def go_exchange_rates(str_date_send):
    access_key = os.environ['CURRENCY_API']
    response = requests.get(f'{URL_CURRENCY}?access_key={access_key}&date={str_date_send}&source={CURRENCY}')
    if response:
        exchange_rates = response.json()
        return exchange_rates
    else:
        get_color_message(('Ошибка получения данных'), 'error')
        logging.warning(response.status_code)
        code = 700
        save_error_currency(code)
        return None
    

def get_exchange_rate(str_date_send):
    for i in range(6):
        report = go_exchange_rates(str_date_send)
        if report is None or report['success']:
            return report
            break
        
    get_color_message(('Сетевая ошибка курса валют'), 'error')
    code = report['error']['code']
    save_error_currency(code)
    return None
