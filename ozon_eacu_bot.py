import dateparser, logging, os
from dotenv import load_dotenv
from script import getting_sales_data
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
        '"день.месяц.год"',
        reply_markup = ReplyKeyboardRemove()
    )
    return "beginning"


def report_beginning(update, context):
    date_beginning = update.message.text
    # try:
    context.user_data["report"] = {"beginning": date_beginning}
    update.message.reply_text(
        'Введите дату конца периода в формате'
        '"день.месяц.год"'
    )
    return "end"
    # except ERROR:
    #     update.message.reply_text("Введите корректную дату")
    #     return "beginning"

# Я пока не могу сообразить, как лучше обработать вводимые данные на корректность.
# Может нужно перенести обработку dateparser'ом из функции take_report сюда и проверить уже данные посе dateparser'а?
# Если да, то проверить через try/except, как у меня заготовлен шаблон выше?
# Не очень понятно тогда, что же делает fallbacks

def report_end(update, context):
    date_end = update.message.text
    # try:
    context.user_data["report"] = {"end": date_end}
    update.message.reply_text("Введите значение лимита от 1 до 1000")
    return "limit"
    # except ERROR:
    #     update.message.reply_text("Введите корректную дату")
    #     return "end"

# Вопросы аналогичны тем, что выше

def report_limit(update, context):
    ozon_limit = update.message.text
    # try:
    context.user_data["report"] = {"limit": ozon_limit}
    update.message.reply_text("Введите значение смещения")
    return "offset"
    # except ERROR:
    #     update.message.reply_text("Введите число от 1 до 1000")
    #     return "limit"

# Тут просто через if/else сделать?

def report_offset(update, context):
    ozon_offset = update.message.text
    # try:
    context.user_data["report"] = {"offset": ozon_offset}
    update.message.reply_text(reply_markup = main_keyboard())
    return ConversationHandler.END
    # except ERROR:
    #     update.message.reply_text("Введите целое положительное число")
    #     return "offset"

# По оффсету ещё у Стаса уточню. Там, как я понимаю, должна быть просто проверка на целое положительное число? 

def take_report(update, context):
    date_start = dateparser.parse(date_beginning, settings = {'DATE_ORDER': 'DMY'})
    date_finish = dateparser.parse(date_end, settings = {'DATE_ORDER': 'DMY'})
    limit = ozon_limit
    offset = ozon_offset
    report_output = getting_sales_data(date_start, date_finish, limit, offset)
    update.message.reply_text(report_output)

# Как вытащить и вставить нужные переменные сюда? Вообще пока не соображаю(((
# Эту функцию нужно вставить в report_offset перед return ConversationHandler.END?
# Как тогда дожен выглядеть в итоге return в report_offset?

def report_incorrect(update, context):
    update.message.reply_text("Введены некорректные данные!")


def command_request(update, context):
    user_text = update.message.text
    update.message.reply_text('Данная команда не поддерживается')

# Если эта функция запускается после /start, но перед нажатием на кнопку "Сформировать отчёт",
# то падает клавиатура, приходится снова вводить /start.
# Куда нужно впихнуть клаву, чтобы она не падала здесь? В update.message.reply_text?

def main():
    ozon_bot = Updater(os.getenv('API_KEY'), use_context = True)

    # Так нужно использовать переменные окружения?

    dp = ozon_bot.dispatcher
    report = ConversationHandler(
        entry_points = [MessageHandler(Filters.regex('^(Сформировать отчёт)$'), report_start)],
        states = {
            "beginning": [MessageHandler(Filters.text, report_beginning)],
            "end": [MessageHandler(Filters.text, report_end)],
            "limit": [MessageHandler(Filters.text, report_limit)],
            "offset": [MessageHandler(Filters.text, report_offset)],
        },
        fallbacks = [MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, report_incorrect)]
    )
    dp.add_handler(report)
    dp.add_handler(CommandHandler('start', greet_user))

    # dp.add_handler(CommandHandler('report', take_report))
    # Этот handler уже не нужен?

    dp.add_handler(MessageHandler(Filters.text, command_request))
    logging.info('BOT STARTED')
    ozon_bot.start_polling()
    ozon_bot.idle()


if __name__ == "__main__":
    main()

# В итоге у меня после прохождения диалога бот прекращает реагировать на любые команды. 
# /start тоже не воспринимает
# Тяжеловато пока даётся понимание бота, долго пытаюсь победить его(
# Ещё и по некотрым урокам по боту код не работает (Clarifai, например), что не добавляет понимания