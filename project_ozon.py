import constants, dateparser, json, logging, ozon_settings
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater


logging.basicConfig(filename='ozon.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s [%(levelname)s]: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')


def greet_user(update, context):
    update.message.reply_text('Здравствуйте, вы используете бота для сбора данных о продажах товаров в страны Таможенного союза через Ozon.\nДля получения отчёта введите команду /report')


def output_report(update, context):
    update.message.reply_text('Введите месяц и год')
    date_input = update.message.text
    update.message.reply_text(collecting_sales(date_input))


def collecting_sales(date):
    formatted_date_input = dateparser.parse(date)
    month_sales = []
    with open("sales.json", "r") as sales:
        sales_list = json.load(sales)    
    for position in sales_list:
        date_import = dateparser.parse(position["date"])
        if date_import.year == formatted_date_input.year and date_import.month == formatted_date_input.month and position["country"] in constants.CUSTOMS_UNION:
            month_sales.append(position)
    return month_sales


def command_request(update, context):
    user_text = update.message.text
    update.message.reply_text('Данная команда не поддерживается. Введите команду /report')


def main():
    mybot = Updater(ozon_settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('report', output_report))
    dp.add_handler(MessageHandler(Filters.text, command_request))
    logging.info('BOT STARTED')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
