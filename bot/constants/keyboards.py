from telegram import InlineKeyboardButton

from constants import callback_data

START_KEYBOARD = [
    [InlineKeyboardButton(
        'Подписаться тут',
        url="https://t.me/dbfsfg"
    )],
    [InlineKeyboardButton(
        'Я подписался, запустить бота',
        callback_data=callback_data.CHECK_SUBSCRIPTION
    )],
]

MENU_BUTTON = [
    [InlineKeyboardButton(
        'Перейти в меню',
        callback_data=callback_data.MENU
    )],
]

MENU_KEYBOARD = [
    [InlineKeyboardButton(
        'Парсер позиций',
        callback_data=callback_data.GET_POSITION
    )],
    [InlineKeyboardButton(
        'Парсер остатков',
        callback_data=callback_data.GET_STOCK
    )],
    [InlineKeyboardButton(
        'Отслеживание коэффицианта приемки WB',
        callback_data=callback_data.GET_RATE
    )],
    [InlineKeyboardButton(
        'Мои подписки на позиции',
        callback_data=callback_data.GET_POSITION_SUBSCRIPTIONS
    )],
]

CANCEL_BUTTON = [
    [InlineKeyboardButton(
        'Отмена',
        callback_data=callback_data.CANCEL
    )],
]

POSITION_CANCEL_BUTTON = [
    [InlineKeyboardButton(
        'Отмена',
        callback_data=callback_data.CANCEL_POSITION
    )],
]

POSITION_REQUEST_BUTTON = [
    [InlineKeyboardButton(
        'Отправить еще запрос',
        callback_data=callback_data.GET_POSITION,
    )],
]

POSITION_SUBSCRIPTION_KEYBOARD = [
    [InlineKeyboardButton(
        'Подписаться на обновления с интервалом:',
        callback_data='no action'
    )],
    [
        InlineKeyboardButton('1 час', callback_data=callback_data.SUBSCRIB1),
        InlineKeyboardButton('6 часов', callback_data=callback_data.SUBSCRIB6),
        InlineKeyboardButton('12 часов', callback_data=callback_data.SUBSCRIB12)
    ],
    [InlineKeyboardButton(
        'Перейти в меню',
        callback_data=callback_data.CANCEL
    )],
]
