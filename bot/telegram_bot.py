from telegram.ext import Application, CommandHandler
from config import bot_token
import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


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
    bot.add_handler(CommandHandler("start", start))
    bot.run_polling()


if __name__ == '__main__':
    main()
