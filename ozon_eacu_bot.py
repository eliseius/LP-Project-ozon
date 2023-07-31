import logging

from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater

from constants import API_KEY_BOT
from handlers import has_incorrect_input, start_bot
from report import (get_report_date_end, get_report_date_start, get_report_incorrect,
                    get_report_start, get_report_status)


logging.basicConfig(
    filename = 'ozon.log',
    level = logging.INFO,
    format = '%(asctime)s - %(name)s [%(levelname)s]: %(message)s',
    datefmt = '%d/%m/%Y %H:%M:%S',
)


def main():
    ozon_bot = Updater(API_KEY_BOT, use_context = True)
    dp = ozon_bot.dispatcher
    report = ConversationHandler(
        entry_points = [MessageHandler(Filters.regex('^(Сформировать отчёт)$'), get_report_start)],
        states = {
            'period_start': [MessageHandler(Filters.text, get_report_date_start)],
            'period_end': [MessageHandler(Filters.text, get_report_date_end)],
            'status': [MessageHandler(Filters.text, get_report_status)],
        },
        fallbacks = [MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, get_report_incorrect)],
    )
    dp.add_handler(report)
    dp.add_handler(CommandHandler('start', start_bot))
    dp.add_handler(MessageHandler(Filters.text, has_incorrect_input))
    logging.info('BOT STARTED')
    ozon_bot.start_polling()
    ozon_bot.idle()


if __name__ == '__main__':
    main()
