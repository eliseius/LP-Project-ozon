URL = 'https://api-seller.ozon.ru/v3/posting/fbs/list'
LIMIT = 1000


DATEPARSER_SETTINGS = {'DATE_ORDER': 'YMD'}


CITIES_FROM_KZ = {'Актау', 'Актобе', 'Алма-Ата', 'Астана', 'Атырау', 'Караганда', 
                  'Костанай', 'Кызылорда', 'Павлодар', 'Петропавловск', 'Тараз', 
                  'Туркестан', 'Уральск', 'Усть-Каменогорск', 'Казахстан'}


CITIES_FROM_BE = {'Брест', 'Витебск', 'Гомель', 'Гродно', 'Минск', 'Могилев', 'Беларусь'}


STATUS_CATALOGUE = {
    'awaiting_registration': 'Ожидает регистрации',
    'acceptance_in_progress': 'Идёт приёмка',
    'awaiting_approve': 'Ожидает подтверждения',
    'awaiting_packaging': 'Ожидает упаковки',
    'awaiting_deliver': 'Ожидает отгрузки',
    'arbitration': 'Арбитраж',
    'client_arbitration': 'Клиентский арбитраж доставки',
    'delivering': 'Доставляется',
    'driver_pickup': 'У водителя',
    'delivered': 'Доставлено',
    'cancelled': 'Отменено',
    'not_accepted': 'Не принято на сортировочном центре',
    'sent_by_seller': 'Отправлено продавцом',
}
