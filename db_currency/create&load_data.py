import requests

from datetime import datetime as dt
from datetime import timedelta as td

import settings

from constantses import CURRENCY, URL_CURRENCY
from db import db_session
from models import Currency


def save_report_with_currency(date):
    report_rates = get_exchange_rate(date)
    short_report = transform_report(report_rates)
    db_session.bulk_insert_mappings(Currency, short_report)
    db_session.commit()
    

def get_exchange_rate(str_date_send):
    for i in range(10):
        report = go_exchange_rates(str_date_send)
        if report is None or report['success']:
            return report
            break   
    print('Сетевая ошибка курса валют')
    print(report)
    return None


def go_exchange_rates(str_date_send):
    access_key = settings.CURRENCY_API
    response = requests.get(f'{URL_CURRENCY}?access_key={access_key}&date={str_date_send}&source={CURRENCY}')
    if response:
        exchange_rates = response.json()
        return exchange_rates
    else:
        print('Ошибка получения данных')
        return None


def transform_report(report):
    send_report = []
    short_report = {
        'date': report['date'],
        'currency': report['source'],
        'value': '%.2f' % float(report['quotes']['USDRUB']),
    }
    send_report.append(short_report)
    return send_report


def get_date(str_date, date_finish):
    date_start = dt.strptime(str_date, '%Y-%m-%d').date()
    date_send = date_start

    while True:
        if date_send > date_finish:
            print(f'Последняя дата:{date_send}')
            break
        else:
            save_report_with_currency(date_send)
            date_send = date_send + td(days=1)


if __name__ == '__main__':
    date_finish = dt.now().date()
    date_send = get_date(settings.STR_DATE_START, date_finish)