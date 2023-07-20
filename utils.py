import constants, dateparser
from telegram import ReplyKeyboardMarkup


def main_keyboard():
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
    if not report_list:
        return ('Нет заказов для отображения в отчёте')
    final_report = []
    for order in report_list:
        final_report.append(
            f'<b>Номер отправления:</b>  {order["posting_number"]}\n'
            f'<b>Дата отгрузки:</b>  {order["shipment_date"]}\n'
            f'<b>Цена:</b>  {order["price"]}\n'
            f'<b>Наименование:</b>  {order["name"]}\n'
            f'<b>Количество:</b>  {order["quantity"]}\n'
            f'<b>Кластер доставки:</b>  {order["cluster_delivery"]}\n'
        )
    return '\n'.join(final_report)
