from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CommandHandler


async def show_stock(update, context):
    """Функция-обработчик для команды /stock"""
    message = (
        "Отправьте артикул для вывода остатков:\n\n"
        "Например:\n"
        "36704403"
    )
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton('Отмена')]],
        one_time_keyboard=True,
        resize_keyboard=True,
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_markup=keyboard
    )


def stock_handlers(app):
    app.add_handler(CommandHandler("stock", show_stock))
