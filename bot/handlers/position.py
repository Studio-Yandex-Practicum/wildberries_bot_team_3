from telegram import InlineKeyboardMarkup
from telegram.ext import MessageHandler, CallbackQueryHandler, filters

from constants import callback_data, keyboards, messages
from services.services import position_parser, position_parser_subscribe


async def position_callback(update, context):
    """Функция-обработчик для кнопки Парсер позиций."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.POSITION_MESSAGE,
        reply_markup=InlineKeyboardMarkup(keyboards.CANCEL_BUTTON)
    )


async def position_parser_callback(update, context):
    """Функция-обработка запроса пользователя"""
    result = await position_parser(update)
    text_split = update.message.text.split()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.POSITION_REQUEST_MESSAGE.format(
            text_split[0], ' '.join(text_split[1:])
        ),
        reply_markup=InlineKeyboardMarkup(keyboards.POSITION_REQUEST_BUTTON),
        parse_mode='Markdown'
    )
    await position_result(update, context, result)


async def position_result(update, context, result):
    """Функция-вывод результата парсинга и кнопки Подписки(1/6/12ч)"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.POSITION_RESULT_MESSAGE.format(result),
        reply_markup=InlineKeyboardMarkup(keyboards.POSITION_SUBSCRIPTION_KEYBOARD)
    )


async def send_position_parser_subscribe(update, context):
    """Функция-проверки подписки на периодичный парсинг (1/6/12ч)"""
    frequency = await position_parser_subscribe(update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.POSITION_SUBSCRIBE_MESSAGE.format(frequency),
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON)
    )


def position_handlers(app):
    app.add_handler(CallbackQueryHandler(position_callback, pattern=callback_data.GET_POSITION))
    app.add_handler(MessageHandler(filters.Regex(r'^\d+(\s\w*)*'), position_parser_callback))
