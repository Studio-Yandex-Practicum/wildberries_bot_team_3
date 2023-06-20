import asyncio
import logging

import aiohttp
from telegram import InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler

from config import TELEGRAM_TOKEN
from constants.data_constants import COMMAND_NAME, TELEGRAM_CHANEL_SUBSCRIBE
from constants.messages import START_BOT_DESCRIPTION_MESSAGE, START_MESSAGE
from handlers.menu import menu_handlers
from handlers.registration import registration_handlers
from keyboards import (
    start_keyboard,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def set_bot_description():
    method = "setMyDescription"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"
    data = {"description": START_BOT_DESCRIPTION_MESSAGE.format(COMMAND_NAME)}
    async with aiohttp.ClientSession() as session:
        async with await session.post(url, json=data) as response:
            if response.status == 200:
                logger.info("Описание успешно установлено.")
            else:
                logger.info("Ошибка при установке описания")


async def start(update, context):
    """Функция-обработчик для команды /start"""
    await context.bot.send_message(
        update.effective_chat.id,
        text=START_MESSAGE.format(TELEGRAM_CHANEL_SUBSCRIBE),
        reply_markup=InlineKeyboardMarkup(start_keyboard)
    )


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_bot_description())
    bot = Application.builder().token(TELEGRAM_TOKEN).build()
    bot.add_handler(CommandHandler('start', start))

    logger.info("Бот успешно запущен.")
    menu_handlers(bot)
    registration_handlers(bot)
    bot.run_polling()


if __name__ == '__main__':
    main()
