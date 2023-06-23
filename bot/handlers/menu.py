from telegram import InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, MessageHandler
from telegram.ext import filters
from constants.constants import BOT_NAME
from constants.messages import (
    HELLO_MESSAGE,
    LEFTOVERS_PARSER_MESSAGE,
    POSITION_PARSER_MESSAGE,
    SUBSCRIPTIONS_MESSAGE,
    UNKNOWN_COMMAND_MESSAGE
)
from keyboards import (
    leftovers_keyboard_input,
    main_keyboard,
    menu_keyboard,
    parsing_keyboard_input,
)


async def main_menu(update, context):
    """Функция-обработчик главного меню."""
    await context.bot.send_message(
        update.effective_chat.id,
        text=HELLO_MESSAGE.format(BOT_NAME),
        reply_markup=InlineKeyboardMarkup(main_keyboard)
    )


async def position_parser_info(update, context):
    """Функция-обработчик для кнопки Парсер позиций."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=POSITION_PARSER_MESSAGE,
        reply_markup=InlineKeyboardMarkup(parsing_keyboard_input)
    )


async def remainder_parser_info(update, context):
    """Функция-обработчик для кнопки Парсер остатков."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=LEFTOVERS_PARSER_MESSAGE,
        reply_markup=InlineKeyboardMarkup(leftovers_keyboard_input)
    )


async def unknown(update, context):
    """Функция-обработчик неизвестных боту команд."""
    await main_menu(update, context, message=UNKNOWN_COMMAND_MESSAGE)


async def get_subscriptions(update, context):
    """Функция-обработчик для кнопки Мои подписки на позиции."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=SUBSCRIPTIONS_MESSAGE,
        reply_markup=InlineKeyboardMarkup(menu_keyboard)
    )


def menu_handlers(app: Application) -> Application:
    app.add_handler(CallbackQueryHandler(main_menu, 'main_menu'))
    app.add_handler(
        CallbackQueryHandler(position_parser_info, 'position_parser')
    )
    app.add_handler(
        CallbackQueryHandler(remainder_parser_info, 'remainder_parser')
    )
    app.add_handler(
        CallbackQueryHandler(get_subscriptions, 'position_subscriptions')
    )
    app.add_handler(
        CallbackQueryHandler(position_parser_info, 'another_parsing_request')
    )
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
