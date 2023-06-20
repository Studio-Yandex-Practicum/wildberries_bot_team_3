import aiohttp
from aiohttp import ClientSession


from config import chat_id, bot_url
from keyboards import subscribe_keyboard, start_keyboard, SUBSCRIBE
from telegram.ext import CallbackQueryHandler

from constants.messages import FALSE_SUBSCRIBE_MESSAGE, TO_MAIN_MENU_MESSAGE


async def get(url, data):
    async with ClientSession() as session:
        async with session.get(url=url, data=data) as response:
            data = await response.json()
            return data


async def check_start_subscription(update, context):
    """Функция-проверки и внесения в БД нового подписчика"""
    CHAT_ID = chat_id
    USER_ID = update.effective_user.id
    chat = update.effective_chat
    url = bot_url
    data = {"chat_id": f"{CHAT_ID}", "user_id": f"{USER_ID}"}
    subscribe = await get(url, data)
    if subscribe["result"]["status"] == "member":
        await context.bot.send_message(chat_id=chat.id,
                                       text = TO_MAIN_MENU_MESSAGE,
                                       reply_markup = start_keyboard()
                                       )
    elif subscribe["result"]["status"] == "left":
        await context.bot.send_message(
            chat_id=chat.id,
            text=FALSE_SUBSCRIBE_MESSAGE,
            reply_markup=subscribe_keyboard(),
        )


def registration_handlers(app):
    app.add_handler(CallbackQueryHandler(check_start_subscription, pattern=SUBSCRIBE))

