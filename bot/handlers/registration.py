from aiohttp import ClientSession

from telegram.ext import CallbackQueryHandler

from config import CHAT_ID, BOT_URL
from constants.buttons import subscribe_message, main_menu, SUBSCRIBE
from constants.messages import FALSE_SUBSCRIBE_MESSAGE, TO_MAIN_MENU_MESSAGE


async def get(url, data):
    async with ClientSession() as session:
        async with session.get(url=url, data=data) as response:
            data = await response.json()
            return data


async def check_start_subscription(update, context):
    """Функция-проверки и внесения в БД нового подписчика"""
    user_id = update.effective_user.id
    chat = update.effective_chat
    data = {"chat_id": f"{CHAT_ID}", "user_id": f"{user_id}"}
    subscribe = await get(BOT_URL, data)
    if subscribe["result"]["status"] == "member":
        await context.bot.send_message(
            chat_id=chat.id,
            text=TO_MAIN_MENU_MESSAGE,
            reply_markup=main_menu()
        )
    elif subscribe["result"]["status"] == "left":
        await context.bot.send_message(
            chat_id=chat.id,
            text=FALSE_SUBSCRIBE_MESSAGE,
            reply_markup=subscribe_message(),
        )


def registration_handlers(app):
    app.add_handler(
        CallbackQueryHandler(check_start_subscription, pattern=SUBSCRIBE)
    )
