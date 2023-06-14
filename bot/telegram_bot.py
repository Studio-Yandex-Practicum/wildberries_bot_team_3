import logging
import re

from config import bot_token
from constants import POSITION_MESSAGE, POSITION_PATTERN, UNKNOWN_COMMAND_TEXT
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update, context):
    """Функция-обработчик для команды /start"""
    start_message = (
        "Привет! Чтобы воспользоваться ботом, нужно подписаться на наш " "telegram канал https://t.me/mpexperts"
    )
    ReplyKeyboardMarkup([[KeyboardButton("/start")]], one_time_keyboard=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_message,
        reply_markup=ReplyKeyboardRemove(),
    )


async def position(update, context):
    """Функция-обработчик для команды /position"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=POSITION_MESSAGE)


async def echo(update, context):
    """Функция-обработчик текста"""
    text = update.message.text
    if not re.match(POSITION_PATTERN, text):
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Нет действий с текстом: {text}")
    result = re.search(POSITION_PATTERN, text)
    articul = result.group("articul")
    name = result.group("name")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Артикул: {articul}, название: {name}")


async def unknown(update, context):
    """Функция-обработчик неизвестных боту команд."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=UNKNOWN_COMMAND_TEXT)


def main():
    """Создаём в директории bot файл config.py и прописываем туда"""
    """bot_token = "ВАШ_ТОКЕН_ОТ_БОТА" """
    token = bot_token
    bot = Application.builder().token(token).build()
    logger.info("Бот успешно запущен.")
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("position", position))
    bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    bot.add_handler(MessageHandler(filters.COMMAND, unknown))
    bot.run_polling()


if __name__ == "__main__":
    main()
