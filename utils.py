import constants
import dateparser
import logging
import os

from telegram import ParseMode, ReplyKeyboardMarkup


def compose_keyboard():
    return ReplyKeyboardMarkup([['Сформировать отчёт',]])


def parse_date(input_date):
    parsed_date = dateparser.parse(input_date, settings = constants.DATEPARSER_SETTINGS)
    return parsed_date
    
    
def render_statuses():
    status_list = []
    status_items = constants.STATUS_CATALOGUE.items()
    for status, value in status_items:
        status_list.append(f'<b>{status}</b>  -  {value}')
    return '\n'.join(status_list)


def render_report(report_list):
    final_report = []
    for order in report_list:
        final_report.append(
            f'<b>Номер отправления:</b>  {order["posting_number"]}\n'
            f'<b>Дата отгрузки:</b>  {order["shipment_date"]}\n'
            f'<b>Цена в долларах:</b>  {order["price_USD"]}\n'
            f'<b>Наименование:</b>  {order["name"]}\n'
            f'<b>Количество:</b>  {order["quantity"]}\n'
            f'<b>Кластер доставки:</b>  {order["cluster_delivery"]}\n'
        )
    return '\n'.join(final_report)


def adapt_sum_post(report_list):
    sum_post = []
    for k, v in report_list.items():
        sum_post.append(
            f'{k} - {v} отправления(ий)'
        )
    return '\n'.join(sum_post)


def output_report(report, sum_post_in_city, update):
    update.message.reply_text(render_report(report), parse_mode = ParseMode.HTML)
    update.message.reply_text(adapt_sum_post(sum_post_in_city))


def save_error_ozon(code):
    name_error = constants.LIST_ERROR_OZON[code]
    text = f'Возникла ошибка OZON\n{code}: {name_error}'
    error_log = f'Error OZON - {code}'
    write_error(text, error_log)


def save_error_currency(code):
    name_error = constants.LIST_ERROR_CURRENCY[code]
    text = f'Возникла ошибка курса валют\n{code}: {name_error}'
    error_log = f'Error CURRENCY - {code}'
    write_error(text, error_log)


def write_error(name, error_log):
    logging.warning(error_log)
    with open(constants.NAME_FILE_WITH_ERROR, 'w', encoding='utf-8') as file:
        file.write(name)



def output_error(update):
    with open(constants.NAME_FILE_WITH_ERROR, 'r', encoding='utf-8') as file:
        name_error = file.read()
    update.message.reply_text(name_error)
    os.remove(constants.LOCATE_FILE_WITH_ERROR)
