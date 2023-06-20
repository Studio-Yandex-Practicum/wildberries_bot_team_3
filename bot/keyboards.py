from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from constants.callback_data import NONSUBSCRIBE, SUBSCRIBE, MAIN_MENU


main_keyboard = [
    [InlineKeyboardButton('Парсер позиций', callback_data='position_parser')],
    [InlineKeyboardButton(
        'Парсер остатков', callback_data='remainder_parser'
    )],
    [InlineKeyboardButton(
        'Отслеживание коэффицианта приемки WB', callback_data='acceptance_rate'
    )],
    [InlineKeyboardButton(
        'Мои подписки на позиции', callback_data='position_subscriptions'
    )],
]
parsing_subscription_keyboard = [
    [InlineKeyboardButton(
        'Подписаться на обновления с интервалом:', callback_data='no action'
    )],
    [
        InlineKeyboardButton('1 час', callback_data='subscribe 1'),
        InlineKeyboardButton('6 часов', callback_data='subscribe 2'),
        InlineKeyboardButton('12 часов', callback_data='subscribe 3')
    ],
    [InlineKeyboardButton('Меню', callback_data='main_menu')],
]
parsing_keyboard_input = [
    [InlineKeyboardButton('Отмена', callback_data='main_menu')],
]
parsing_keyboard_expectation = [
    [InlineKeyboardButton(
        'Отправить еще запрос',
        callback_data='another_parsing_request',
    )],
]
leftovers_keyboard_input = [
    [InlineKeyboardButton('Отмена', callback_data='main_menu')],
]
menu_keyboard = [
    [InlineKeyboardButton('Меню', callback_data='main_menu')],
]

def subscribe_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Подписаться тут", callback_data=NONSUBSCRIBE, url="https://t.me/dbfsfg"),
            ],
            [
                InlineKeyboardButton(text='Я уже подписан', callback_data=SUBSCRIBE),
            ],
        ]
    )

def start_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Я подписался, запустить бота', callback_data=MAIN_MENU)
            ],
        ]    
    )