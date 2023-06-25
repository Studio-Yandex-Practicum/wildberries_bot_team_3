from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters

from keyboards import menu_keyboard
from constants.constants import POSITION_MESSAGE
from constants.messages import LEFTOVERS_PARSER_RESULT_MESSAGE
from services.services import remainder_parser


async def position(update, context):
    """Функция-обработчик для команды /position"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=POSITION_MESSAGE
    )


async def remainder_parser_result(update, context):
    """Функция-вывода результатов парсинга по артикулу"""
    result = await remainder_parser(update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=LEFTOVERS_PARSER_RESULT_MESSAGE.format(result),
        reply_markup=InlineKeyboardMarkup(menu_keyboard)
    )


def position_handlers(app):
    app.add_handler(CommandHandler("position", position))
    app.add_handler(
        MessageHandler(filters.Regex(r'^\d+$'), remainder_parser_result)
    )
