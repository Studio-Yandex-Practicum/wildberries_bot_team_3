import asyncio
import logging

import aiohttp
from telegram.ext import Application, CommandHandler

from config import bot_token
from constants.buttons import subscribe_message
from constants.messages import START_BOT_DESCRIPTION_MESSAGE, START_MESSAGE
from handlers import rate, registration
from handlers.menu import menu_handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def set_bot_description():
    """Функция изменения описания бота перед запуском."""
    method = 'setMyDescription'
    url = f'https://api.telegram.org/bot{bot_token}/{method}'
    data = {'description': START_BOT_DESCRIPTION_MESSAGE}
    async with aiohttp.ClientSession() as session:
        async with await session.post(url, json=data) as response:
            if response.status == 200:
                logger.info('Описание успешно установлено')
            else:
                logger.info('Ошибка при установке описания')


async def start(update, context):
    """Функция-обработчик для команды /start."""
    chat = update.effective_chat
    await context.bot.send_message(
        chat_id=chat.id,
        text=START_MESSAGE,
        reply_markup=subscribe_message(),
    )


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_bot_description())
    bot = Application.builder().token(bot_token).build()
    logger.info('Бот успешно запущен.')
    bot.add_handler(CommandHandler('start', start))
    registration.registration_handlers(bot)
    rate.rate_handlers(bot)
    menu_handlers(bot)
    bot.run_polling()


if __name__ == '__main__':
    main()
