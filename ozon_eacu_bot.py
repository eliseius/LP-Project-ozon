import constants, dateparser, logging, os
from dotenv import load_dotenv
from script import get_sales_data
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Filters, Updater, CommandHandler, ConversationHandler, MessageHandler


load_dotenv()


logging.basicConfig(
    filename = 'ozon.log',
    level = logging.INFO,
    format = '%(asctime)s - %(name)s [%(levelname)s]: %(message)s',
    datefmt = '%d/%m/%Y %H:%M:%S'
)


def main_keyboard():
    return ReplyKeyboardMarkup([['Сформировать отчёт']])


def greet_user(update, context):
    update.message.reply_text(
        'Здравствуйте, вы используете бота для сбора данных о продажах товаров в страны Таможенного союза через Ozon.'
        'Для получения отчёта нажмите кнопку "Сформировать отчёт"',
        reply_markup = main_keyboard()
    )


def report_start(update, context):
    update.message.reply_text(
        'Введите дату начала периода в формате'
        '"год.месяц.день"',
        reply_markup = ReplyKeyboardRemove()
    )
    return "beginning"


def report_beginning(update, context):
    date_beginning = get_date(update.message.text)
    if date_beginning is not None:
        context.user_data["report"] = {"beginning": date_beginning}
        update.message.reply_text(
            'Введите дату конца периода в формате'
            '"год.месяц.день"'
        )
        return "end"
    else:
        update.message.reply_text("Введите корректную дату")
        return "beginning"


def report_end(update, context):
    date_end = get_date(update.message.text)
    if date_end is not None:
        context.user_data["report"] = {"end": date_end}
        update.message.reply_text("Введите статус заказов")
        return "status"
    else:
        update.message.reply_text("Введите корректную дату")
        return "end"


def report_status(update, context):
    order_status = update.message.text
    if order_status in constants.STATUS_CATALOGUE:
        context.user_data["report"] = {"status": order_status}
        update.message.reply_text("Отчёт готов")
        return "save"
    else:
        update.message.reply_text("Введите корректный статус заказов")
        return "status"


def report_save(update, context):
    report_output = get_sales_data("beginning", "end", "status")
    # report_output = get_sales_data(date_beginning, date_end, order_status)
    update.message.reply_text(report_output)
    return "new"


def new_report(update, context):
    update.message.reply_text(
        'Вы можете сформировать новый отчёт',
        reply_markup = main_keyboard()
    )


def report_incorrect(update, context):
    update.message.reply_text("Введены некорректные данные!")


def command_request(update, context):
    user_text = update.message.text
    update.message.reply_text(
        'Данная команда не поддерживается',
        reply_markup = main_keyboard()
    )


def get_date(input_date):  
    parsed_date = dateparser.parse(input_date, settings = {'DATE_ORDER': 'YMD'})
    return parsed_date


def main():
    ozon_bot = Updater(os.getenv('API_KEY'), use_context = True)
    dp = ozon_bot.dispatcher
    report = ConversationHandler(
        entry_points = [MessageHandler(Filters.regex('^(Сформировать отчёт)$'), report_start)],
        states = {
            "beginning": [MessageHandler(Filters.text, report_beginning)],
            "end": [MessageHandler(Filters.text, report_end)],
            "status": [MessageHandler(Filters.text, report_status)],
            "save": [MessageHandler(Filters.text, report_save)],
            "new": [MessageHandler(Filters.text, new_report)]
        },
        fallbacks = [MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, report_incorrect)]
    )
    dp.add_handler(report)
    dp.add_handler(CommandHandler('start', greet_user))
    # dp.add_handler(CommandHandler('report', take_report))
    dp.add_handler(MessageHandler(Filters.text, command_request))
    logging.info('BOT STARTED')
    ozon_bot.start_polling()
    ozon_bot.idle()


if __name__ == "__main__":
    main()
