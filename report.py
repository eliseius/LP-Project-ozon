import constants
from script import get_sales_data
from telegram import ParseMode, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from utils import get_date, print_report, print_statuses, show_main_keyboard


def get_report_start(update, context):
    update.message.reply_text(
        'Введите дату начала периода в формате\n'
        '"год.месяц.день"',
        reply_markup = ReplyKeyboardRemove(),
    )
    return 'period_beginning'


def get_report_date1(update, context):
    date_beginning = get_date(update.message.text)
    if date_beginning is None:
        update.message.reply_text('Введите корректную дату')
        return 'period_beginning'
    context.user_data['report'] = {'period_beginning': date_beginning}
    update.message.reply_text(
        'Введите дату конца периода в формате\n'
        '"год.месяц.день"'
    )
    return 'period_end'


def get_report_date2(update, context):
    date_end = get_date(update.message.text)
    if date_end is None:
        update.message.reply_text('Введите корректную дату')
        return 'period_end'
    if date_end <= context.user_data['report']['period_beginning']:
        update.message.reply_text('Дата конца периода не может быть раньше даты начала')
        return 'period_end'
    context.user_data['report']['period_end'] = date_end
    update.message.reply_text('Введите статус заказов')
    update.message.reply_text(f'Доступные статусы:\n\n{print_statuses()}', parse_mode = ParseMode.HTML)
    return 'status'


def get_report_status(update, context):
    order_status = update.message.text
    if order_status not in constants.STATUS_CATALOGUE:
        update.message.reply_text('Введите корректный статус заказов')
        return 'status'
    # context.user_data['report']['status'] = order_status
    date_start = context.user_data['report']['period_beginning']
    date_finish = context.user_data['report']['period_end']
    update.message.reply_text('Отчёт формируется...')
    report_output = get_sales_data(date_start, date_finish, order_status)
    update.message.reply_text(print_report(report_output), parse_mode = ParseMode.HTML)
    update.message.reply_text(
        'Вы можете сформировать новый отчёт',
        reply_markup = show_main_keyboard(),
    )
    return ConversationHandler.END


def get_report_incorrect(update, context):
    update.message.reply_text('Введены некорректные данные')
