URL_OZON = "https://api-seller.ozon.ru/v3/posting/fbs/list"
LIMIT = 1000

CITIES_FROM_KZ = {'Актау', 'Актобе', 'Алма-Ата', 'Астана', 'Атырау', 'Караганда', 
                  'Костанай', 'Кызылорда', 'Павлодар', 'Петропавловск', 'Тараз', 
                  'Туркестан', 'Уральск', 'Усть-Каменогорск', 'Казахстан'}


CITIES_FROM_BE = {'Брест', 'Витебск', 'Гомель', 'Гродно', 'Минск', 'Могилев','Беларусь'}


STATUS_CATALOGUE = {'awaiting_registration', 'acceptance_in_progress', 'awaiting_approve', 
                    'awaiting_packaging', 'awaiting_deliver', 'arbitration', 'client_arbitration', 
                    'delivering', 'driver_pickup', 'delivered', 'cancelled', 
                    'not_accepted', 'sent_by_seller'
                    }

URL_CURRENCY = "http://api.currencylayer.com/historical"

LIST_ERROR_OZON = {
                    400: 'Неверный параметр. Обратитесь в службу поддержки бота.',#Возникает, если не правильно переданы limit, offset или status
                    403: 'Доступ запрещен. Неправильные Client-Id или Api-Key.',
                    404: 'Ответ не найден. Обратитесь в службу поддержки бота.', #Неправильное или неполное наименование метода.
                    409: 'Конфликт запроса',
                    500: 'Внутренняя ошибка сервиса. Попробуйте сделать запрос позже.',
                    700: 'Ошибка сформированных данных. Обратитесь в службу поддержки бота.',
}
