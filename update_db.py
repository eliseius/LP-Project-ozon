import logging
import os
import requests
import schedule
import time

from datetime import datetime as dt
from datetime import timedelta as td

import db_currency.settings

from db_currency.constantses import CURRENCY, URL_CURRENCY
from db_currency.db import db_session
from db_currency.models import Currency
from utils import save_error_currency


def get_last_date():
    try:
        query = Currency.query.order_by(Currency.date.desc()).first()
        return query.date
    except:
        code = 808
        save_error_currency(code)
        return None


def update_db():
    last_date = get_last_date()
    date_now = dt.now().date()
    while True:
        date_send = last_date + td(days=1)
        if date_now > date_send:
            add_data_in_db(date_send)
        else:
            break
        last_date = date_send


def add_data_in_db(date):
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
    code = report['error']['code']
    save_error_currency(code)
    return None


def go_exchange_rates(str_date_send):
    access_key = os.environ['CURRENCY_API'] # access_key = db_currency.settings.CURRENCY_API
    response = requests.get(f'{URL_CURRENCY}?access_key={access_key}&date={str_date_send}&source={CURRENCY}')
    if response:
        exchange_rates = response.json()
        return exchange_rates
    else:
        print('Ошибка получения данных')
        logging.error(response.status_code)
        code = 700
        save_error_currency(code)
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


def start_update_dbase():
    minute_start = 1# изменить время после первого обращения в бд
    schedule.every(minute_start).minutes.do(update_db)

    while True:
        schedule.run_pending()
        time.sleep(1)
