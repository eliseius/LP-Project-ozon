from utils import compose_keyboard


def start_bot(update, context):
    update.message.reply_text(
        'Здравствуйте, вы используете бота для сбора данных '
        'о продажах товаров в страны Таможенного союза через Ozon.\n'
        'Для получения отчёта нажмите кнопку "Сформировать отчёт"',
        reply_markup = compose_keyboard(),
    )


def has_incorrect_input(update, context):
    update.message.reply_text('Данная команда не поддерживается')
