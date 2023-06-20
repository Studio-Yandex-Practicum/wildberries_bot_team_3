import asyncio
import logging

import aiohttp
from telegram import InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from config import TELEGRAM_TOKEN
from constants.data_constants import (
    BOT_NAME, COMMAND_NAME, TELEGRAM_CHANEL_SUBSCRIBE
)
from constants.messages import (
    HELLO_MESSAGE, START_BOT_DESCRIPTION_MESSAGE, START_MESSAGE
)
from handlers.menu import (
    menu_handlers,
    main_menu,
    position_parser_info,
    remainder_parser_info,
    acceptance_rate_info,
    get_subscriptions,
    send_position_parser_subscribe
)
from handlers.registration import check_start_subscription
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


async def check_callback(update, context):
    """Функция-обработчик callback запросов"""
    data = update.callback_query.data
    if data == 'main_menu':
        await main_menu(
            update, context, message=HELLO_MESSAGE.format(BOT_NAME)
        )
    elif data == 'check_start_subscription':
        await check_start_subscription(update, context)
    elif data == 'position_parser':
        await position_parser_info(update, context)
    elif data == 'remainder_parser':
        await remainder_parser_info(update, context)
    elif data == 'acceptance_rate':
        await acceptance_rate_info(update, context)
    elif data == 'position_subscriptions':
        await get_subscriptions(update, context)
    elif data == 'another_parsing_request':
        await position_parser_info(update, context)
    else:
        await send_position_parser_subscribe(update, context)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_bot_description())
    bot = Application.builder().token(TELEGRAM_TOKEN).build()
    logger.info("Бот успешно запущен.")
    bot.add_handler(CommandHandler('start', start))
    bot.add_handler(CallbackQueryHandler(check_callback))
    # registration_handlers(bot)
    menu_handlers(bot)
    bot.run_polling()


if __name__ == '__main__':
    main()
