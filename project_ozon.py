import dateparser, logging, ozon_settings
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater


logging.basicConfig(filename='ozon.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s [%(levelname)s]: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')


def greet_user(update, context):
    update.message.reply_text('Здравствуйте, вы используете бота для сбора данных о продажах товаров в страны Таможенного союза через Ozon.\nДля получения отчёта введите команду /report, начало и конец периода в формате "день.месяц.год", разделённые пробелом')


def take_report(update, context):
    date_input = update.message.text
    date_start = dateparser.parse(date_input.split()[1], settings={'DATE_ORDER': 'DMY'})
    date_finish = dateparser.parse(date_input.split()[2], settings={'DATE_ORDER': 'DMY'})
    report_output = general_report_output(date_start, date_finish, limit, offset)
    update.message.reply_text(report_output)


def general_report_output(date_start, date_finish, limit, offset):


def command_request(update, context):
    user_text = update.message.text
    update.message.reply_text('Данная команда не поддерживается. Введите команду /report, начало и конец периода в формате "день.месяц.год", разделённые пробелом')


def main():
    mybot = Updater(ozon_settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('report', take_report))
    dp.add_handler(MessageHandler(Filters.text, command_request))
    logging.info('BOT STARTED')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
