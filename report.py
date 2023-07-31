import constants
import os

from telegram import ParseMode, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from script import get_sales_data
from utils import compose_keyboard, output_error, output_report, parse_date, render_statuses


def get_report_start(update, context):
    update.message.reply_text(
        'Введите дату начала периода в формате\n'
        '"год.месяц.день"',
        reply_markup = ReplyKeyboardRemove(),
    )
    return 'period_start'


def get_report_date_start(update, context):
    date_start = parse_date(update.message.text)
    if date_start is None:
        update.message.reply_text('Введите корректную дату')
        return 'period_start'
    context.user_data['report'] = {'period_start': date_start}
    update.message.reply_text(
        'Введите дату конца периода в формате\n'
        '"год.месяц.день"'
    )
    return 'period_end'


def get_report_date_end(update, context):
    date_end = parse_date(update.message.text)
    if date_end is None:
        update.message.reply_text('Введите корректную дату')
        return 'period_end'
    if date_end <= context.user_data['report']['period_start']:
        update.message.reply_text('Дата конца периода не может быть раньше даты начала')
        return 'period_end'
    context.user_data['report']['period_end'] = date_end
    update.message.reply_text('Введите статус заказов')
    update.message.reply_text(f'Доступные статусы:\n\n{render_statuses()}', parse_mode = ParseMode.HTML)
    return 'status'


def get_report_status(update, context):
    order_status = update.message.text
    if order_status not in constants.STATUS_CATALOGUE:
        update.message.reply_text('Введите корректный статус заказов')
        return 'status'
    update.message.reply_text('Отчёт формируется...')
    report_output, sum_post_in_city = get_sales_data(
        date_start=context.user_data['report']['period_start'],
        date_finish=context.user_data['report']['period_end'],
        status=order_status,
    )
    check_report(report_output, sum_post_in_city, update)
    update.message.reply_text(
        'Вы можете сформировать новый отчёт',
        reply_markup = compose_keyboard(),
    )
    return ConversationHandler.END


def get_report_incorrect(update, context):
    update.message.reply_text('Невозможно обработать объект!\nВведите корректные данные с клавиатуры')


def check_report(report, sum_post_in_city, update):
    if not report:
        if os.path.exists(constants.LOCATE_FILE_WITH_ERROR):
            output_error(update)
        else:
            update.message.reply_text('Нет заказов для отображения в отчёте. Попробуйте ввести другие данные')
    else:
        output_report(report, sum_post_in_city, update)
