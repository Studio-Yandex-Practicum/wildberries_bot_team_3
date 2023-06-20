from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from constants.data_constants import TELEGRAM_CHANEL_SUBSCRIBE

NONSUBSCRIBE = "nonsubscribe"
SUBSCRIBE = "check_start_subscription"
MAIN_MENU = "main_menu"


def subscribe_message():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подписаться тут",
                    callback_data=NONSUBSCRIBE,
                    url=TELEGRAM_CHANEL_SUBSCRIBE
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Я уже подписан',
                    callback_data=SUBSCRIBE
                ),
            ],
        ]
    )


def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    'Перейти в главное меню',
                    callback_data=MAIN_MENU
                ),
            ],
        ]
    )
