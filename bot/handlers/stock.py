from telegram import InlineKeyboardMarkup
from telegram.ext import MessageHandler, filters


from keyboards import menu_keyboard
from constants.messages import LEFTOVERS_PARSER_RESULT_MESSAGE
from services.services import remainder_parser


async def stock_callback(update, context):
    """Функция-вывода результатов парсинга по артикулу"""
    result = await remainder_parser(update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=LEFTOVERS_PARSER_RESULT_MESSAGE.format(result),
        reply_markup=InlineKeyboardMarkup(menu_keyboard)
    )


def stock_handlers(app):
    app.add_handler(MessageHandler(filters.Regex(r'^\d+$'), stock_callback))
