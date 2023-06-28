from telegram import InlineKeyboardMarkup
from telegram.ext import MessageHandler, CallbackQueryHandler, filters

from constants import callback_data, keyboards, messages
from services.services import remainder_parser


async def stock_callback(update, context):
    """Функция-обработчик для кнопки Парсер остатков."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.STOCK_MESSAGE,
        reply_markup=InlineKeyboardMarkup(keyboards.CANCEL_BUTTON)
    )


async def stock_result_callback(update, context):
    """Функция-вывода результатов парсинга по артикулу"""
    result = await remainder_parser(update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.STOCK_RESULT_MESSAGE.format(result),
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON)
    )


def stock_handlers(app):
    app.add_handler(CallbackQueryHandler(stock_callback, pattern=callback_data.GET_STOCK))
    app.add_handler(MessageHandler(filters.Regex(r'^\d+$'), stock_result_callback))
