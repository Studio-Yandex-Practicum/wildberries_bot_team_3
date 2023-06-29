from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, MessageHandler, filters

from constants import callback_data, keyboards, messages
from services.services import ckeck_warehouse_request


async def rate_callback(update, context):
    """Функция-обработчик для кнопки Отслеживание коэффицианта приемки WB"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.RATE_MESSAGE,
        reply_markup=InlineKeyboardMarkup(keyboards.CANCEL_BUTTON)
    )


async def rate_result_callback(update, context):
    """Функция-вывод результата Отслеживание коэффициента приемки WB"""
    result = await ckeck_warehouse_request(update)
    if result is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=messages.UNKNOWN_COMMAND_MESSAGE,
            reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON)
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=messages.RATE_RESULT_MESSAGE,
            reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON)
        )


def rate_handlers(app):
    app.add_handler(
        CallbackQueryHandler(rate_callback, pattern=callback_data.GET_RATE)
    )
    app.add_handler(MessageHandler(filters.TEXT, rate_result_callback))
