from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, MessageHandler, filters

from constants.messages import (
    ACCEPTANCE_RATE_ANSWER_MESSAGE, UNKNOWN_COMMAND_MESSAGE
)
from keyboards import return_menu_keyboard
from services.services import ckeck_warehouse_request


async def rate_callback(update, context):
    """Функция-вывод результата Отслеживание коэффициента приемки WB"""
    result = await ckeck_warehouse_request(update)
    if result is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=UNKNOWN_COMMAND_MESSAGE,
            reply_markup=InlineKeyboardMarkup(return_menu_keyboard)
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ACCEPTANCE_RATE_ANSWER_MESSAGE,
        )


def rate_handlers(app):
    # app.add_handler(MessageHandler(filters.TEXT, rate_callback))
    app.add_handler(CallbackQueryHandler(rate_callback, 'acceptance_rate'))
