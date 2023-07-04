from constants.constant import (BOT_NAME, COMMAND_NAME,
                                TELEGRAM_CHANEL_SUBSCRIBE)

START_BOT_DESCRIPTION_MESSAGE = (
    f'Привет! На связи команда {COMMAND_NAME}\n'
    f'Мы создали этого бота для помощи всем действующим поставщикам '
    f'Wildberries.\n\n'
    f'Здесь вы можете:\n'
    f'- отследить позиции вашей карточки в выдаче.\n'
    f'- увидеть остатки товара по складам\n'
    f'- узнать остатки товара по размерам.\n\n'
    f'Для начала работы нажмите Start'
)
START_MESSAGE = (
    f'Привет! Чтобы воспользоваться ботом, нужно подписаться на наш '
    f'telegram канал {TELEGRAM_CHANEL_SUBSCRIBE}'
)
SUCCESS_SUBSCRIBE_MESSAGE = (
    'Спасибо за подписку! Вы можете воспользоваться меню бота:'
)
FALSE_SUBSCRIBE_MESSAGE = (
    'Вы не подписались на наш telegram канал'
)
HELLO_MESSAGE = (
    f'Добро пожаловать в {BOT_NAME}!\n'
    f'Узнайте на каких позициях находится ваш товар в поиске Wildberries.'
)
POSITION_MESSAGE = (
    'Для определения позиции артикула отправьте сообщение в формате\n'
    '\'Артикул Поисковая фраза\'\n\n'
    'Например:\n36704403 футболка женская'
)
# UNSUBSCRIBE_MESSAGE = (
#     'Для отмены подписки отправьте сообщение в формате\n'
#     '\'Артикул\'\n\n'
#     'Например:\n36704403'
# )
UNSUBSCRIBE_MESSAGE = (
    'Подписка *{}* удалена'
)
SUBSCRIBE_MESSAGE = (
    'Артикул: {}, текст: {}, периодичность {}ч'
)
EMPTY_SUBSCRIBE_MESSAGE = (
    'У Вас нет подписок'
)
POSITION_REQUEST_MESSAGE = (
    'Запрос с артикулом *{}* и поисковой фразой '
    '*{}* создан! В близжайшее время вам будет отправлен результат'
)
POSITION_RESULT_MESSAGE = 'Результат запроса. Товар на {} месте'
POSITION_SUBSCRIBE_MESSAGE = (
    'Вы подписались на обновление каждые {} час(ов)'
)
STOCK_MESSAGE = (
    'Отправьте артикул для вывода остатков:\n'
    'Например:\n'
    '36704403\n'
)
STOCK_RESULT_MESSAGE = 'остатки по складам и по размерам {}'
RATE_MESSAGE = 'Выберите склад:\nНапример:\nАстрахань'
RATE_RESULT_MESSAGE = (
    'Коэффицианта приемки для склада {} составляет {}'
)
SUBSCRIPTIONS_MESSAGE = 'Ваши подписки: {}'
UNKNOWN_COMMAND_MESSAGE = 'Неизвестная команда, воспользуйтесь меню'
TO_MAIN_MENU_MESSAGE = 'Спасибо за подписку!'
CANCEL_MESSAGE = f'Вы находитесь в главном меню бота {BOT_NAME}!'
