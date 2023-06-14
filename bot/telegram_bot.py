import asyncio
import logging
import re

import aiohttp
from aiohttp import ClientSession
from config import bot_token
from constants import (POSITION_MESSAGE, POSITION_PATTERN,
                       UNKNOWN_COMMAND_TEXT, BOT_START_MESSAGE
                       )
from telegram import (KeyboardButton, ReplyKeyboardMarkup,
                      ReplyKeyboardRemove, InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import Application, CommandHandler, MessageHandler, filters

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


SUBSCRIBE = "subscribe"


def subscribe_message():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Подписаться тут", callback_data=SUBSCRIBE, url="https://t.me/dbfsfg"),
            ],
        ]
    )


async def set_bot_description():
    description = (
        "Привет! На связи команда @...\n"
        "Мы создали этого бота для помощи всем действующим поставщикам "
        "Wildberries.\n\n"
        "Здесь вы можете:\n"
        "- отследить позиции вашей карточки в выдаче.\n"
        "- увидеть остатки товара по складам\n"
        "- узнать остатки товара по размерам.\n\n"
        "Для начала работы нажмите Start"
    )
    method = "setMyDescription"
    url = f"https://api.telegram.org/bot{bot_token}/{method}"
    data = {"description": description}
    async with aiohttp.ClientSession() as session:
        async with await session.post(url, json=data) as response:
            if response.status == 200:
                logger.info("Описание успешно установлено")
            else:
                logger.info("Ошибка при установке описания")


async def get(url, data):
    async with ClientSession() as session:
        async with session.get(url=url, data=data) as response:
            data = await response.json()
            return data


async def start(update, context):
    """Функция-обработчик для команды /start.
    Отправляется запрос к API телеграм с запросом
    по конкретной группе(переменная url)
    В переменной data находятся значения для API
    При проверке подписки у автора канала выводится не 'member',
    а 'creator'.
    Если человек подписан, то выводится сообщение 'Вы подписаны',
    В противном случае человеку даётся ссылка на канал и предлагается подписаться.
    """
    CHAT_ID = "@dbfsfg"
    USER_ID = update.effective_user.id
    chat = update.effective_chat
    url = "https://api.telegram.org/bot6094915944:AAEfqdam7pOhgtkO4wEpJKu2UfPvHJ7-tK4/getChatMember"
    data = {"chat_id": f"{CHAT_ID}", "user_id": f"{USER_ID}"}
    subscribe = await get(url, data)
    if subscribe["result"]["status"] == "member":
        await context.bot.send_message(chat_id=chat.id, text="Вы подписаны")
    elif subscribe["result"]["status"] == "left":
        await context.bot.send_message(
            chat_id=chat.id,
            text=BOT_START_MESSAGE,
            reply_markup=subscribe_message(),
        )


# TODO Нужно придумать как поступать после перехода из бота в канал.
# сообщение остаётся висеть или нужно новое или удалить просто всё?


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

    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_bot_description())

    bot = Application.builder().token(token).build()
    logger.info("Бот успешно запущен.")

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("position", position))
    bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    bot.add_handler(MessageHandler(filters.COMMAND, unknown))
    bot.run_polling()


if __name__ == "__main__":
    asyncio.run(main())

# TODO ^^^ Это место обязательно нужно посмотреть
