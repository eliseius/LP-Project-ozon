from datetime import datetime as dt

from db_currency.models import Currency
from utils import save_error_currency


def get_exchange_rate(str_date):
    try:
        query = Currency.query.filter(Currency.date == str_date).first()
        return query.value
    except:
        code = 800
        save_error_currency(code)
        return None


def get_report_with_currency(report):
    for item_sold in report:
        str_shipment_date = item_sold['shipment_date']
        date_shipment = dt.strptime(str_shipment_date, '%Y-%m-%dT%H:%M:%SZ').date()
        str_date_send = dt.strftime(date_shipment, '%Y-%m-%d')
        rate = get_exchange_rate(str_date_send)
        if rate is not None:
            calcuation_usd = round(float(item_sold['price']) / float(rate), 2)
            item_sold['price'] = calcuation_usd
            item_sold['price_USD'] = item_sold.pop('price')
        else:
            print('Ошибка получения валюты')#Обработать ошибку подключения к базе данных и написать в logging
            report = []
    return report
    