import ozon_settings, logging, json
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(filename='ozon.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s [%(levelname)s]: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')


def greet_user(update, context):
    update.message.reply_text('Здравствуйте, вы используете бота для сбора данных о продажах товаров в страны Таможенного союза через Ozon.\nВведите команду /report, месяц и год в формате "мм.гггг" для получения отчёта:')


def collecting_sales (update, context):
    eacu = ["Армения", "Беларусь", "Казахстан", "Киргизия", "Россия"]
    month_sales = []
    date_input = update.message.text.split()[1]
    formatted_date_input = datetime.strptime(date_input, "%m.%Y")
    with open("sales.json", "r") as sales:
        sales_list = json.load(sales)
    for position in sales_list:
        date_from_json = datetime.strptime(position["date"][:10], "%Y-%m-%d")
        if date_from_json.year == formatted_date_input.year and date_from_json.month == formatted_date_input.month and position["country"] in eacu:
            month_sales += position
        update.message.reply_text(month_sales)
        # На данный момент выводит пустой список((( Пока не сообразил, где косяк

def main():
    mybot = Updater(ozon_settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('report', collecting_sales))
    # dp.add_handler(MessageHandler(Filters.text, function))
    logging.info('BOT STARTED')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
