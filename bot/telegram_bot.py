from telegram.ext import (
    Application, CommandHandler, ChatMemberHandler,
)
from config import bot_token
import logging
from telegram import (
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def welcome_new_members(update, context):
    """Приветственное сообщение для новых участников чата"""
    logger.info("welcome_new_members() успешно запущен.")
    welcome_message = (
        "Что умеет этот бот?\n\nПривет! На связи команда @...\n"
        "Мы создали этого бота для помощи всем действующим поставщикам "
        "Wildberries.\n\n"
        "Здесь вы можете:\n"
        "- отследить позиции вашей карточки в выдаче.\n"
        "- увидеть остатки товара по складам\n"
        "- узнать остатки товара по размерам.\n\n"
        "Для начала работы нажмите Start"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=welcome_message,
    )


async def start(update, context):
    """Функция-обработчик для команды /start"""
    start_message = (
        "Привет! Чтобы воспользоваться ботом, нужно подписаться на наш "
        "telegram канал https://t.me/mpexperts"
    )
    ReplyKeyboardMarkup(
        [[KeyboardButton('/start')]],
        one_time_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_message,
        reply_markup=ReplyKeyboardRemove(),
    )


def main():
    """Создаём в директории bot файл config.py и прописываем туда """
    """bot_token = "ВАШ_ТОКЕН_ОТ_БОТА" """
    token = bot_token
    bot = Application.builder().token(token).build()
    logger.info("Бот успешно запущен.")

    bot.add_handler(ChatMemberHandler(
        welcome_new_members, ChatMemberHandler.CHAT_MEMBER
    ))

    bot.add_handler(CommandHandler("start", start))

    bot.run_polling()


if __name__ == '__main__':
    main()
