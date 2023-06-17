from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, MessageHandler, filters

from constants.messages import (ACCEPTANCE_RATE_ANSWER_MESSAGE,
                                ACCEPTANCE_RATE_MESSAGE, ERROR_MESSAGE)
from keyboards import return_menu_keyboard
from services.services import ckeck_warehouse_request


async def acceptance_rate_info(update, context):
    """Функция-обработчик для кнопки Отслеживание коэффицианта приемки WB"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ACCEPTANCE_RATE_MESSAGE,
    )


async def acceptance_rate_answer(update, context):
    """Функция-вывод результата Отслеживание коэффицианта приемки WB"""
    result = await ckeck_warehouse_request(update)
    if result is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ERROR_MESSAGE,
            reply_markup=InlineKeyboardMarkup(return_menu_keyboard)
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ACCEPTANCE_RATE_ANSWER_MESSAGE,
        )


def rate_handlers(app):
    app.add_handler(
        CallbackQueryHandler(
            acceptance_rate_info, pattern="acceptance_rate"
        ))
    app.add_handler(MessageHandler(filters.TEXT, acceptance_rate_answer))
