import asyncio
import logging
import re

import aiohttp
from aiohttp import ClientSession
from telegram import (InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          MessageHandler, filters)

from handlers import registration
from config import bot_token
from constants.constants import (POSITION_MESSAGE, POSITION_PATTERN,
                                 UNKNOWN_COMMAND_TEXT)
from constants.messages import (ACCEPTANCE_RATE_ANSWER_MESSAGE,
                                ACCEPTANCE_RATE_MESSAGE,
                                HELLO_MESSAGE,
                                LEFTOVERS_PARSER_MESSAGE,
                                LEFTOVERS_PARSER_RESULT_MESSAGE,
                                POSITION_PARSER_EXPECTATION_MESSAGE,
                                POSITION_PARSER_MESSAGE,
                                POSITION_PARSER_RESULT_MESSAGE,
                                POSITION_PARSER_SUBSCRIBE_MESSAGE,
                                START_MESSAGE, SUBSCRIPTIONS_MESSAGE)
from keyboards import subscribe_keyboard, MAIN_MENU
from constants.parser_constants import STOCS
from keyboards import (leftovers_keyboard_input, main_keyboard, menu_keyboard,
                       parsing_keyboard_expectation, parsing_keyboard_input,
                       parsing_subscription_keyboard)
from services.services import (acceptance_rate_api, add_to_db, position_parser,
                               position_parser_subscribe, remainder_parser)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


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


async def check_callback(update, context):
    """Функция-обработчик callback запросов"""
    data = update.callback_query.data
    if data == 'main_menu':
        await main_menu(update, context)
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


async def start(update, context):
    """Функция-обработчик для команды /start"""
    chat = update.effective_chat
    await context.bot.send_message(
        chat_id=chat.id,
        text=START_MESSAGE,
        reply_markup=subscribe_keyboard(),
    )


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


async def handle_cancel(update, context):
    """Функция-обработчик для нажатия на кнопку 'Отмена'"""
    message_text = update.message.text
    if message_text == 'Отмена':
        cancel_message = 'Действие отменено'
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=cancel_message
        )


async def position(update, context):
    """Функция-обработчик для команды /position"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=POSITION_MESSAGE
    )


async def echo(update, context):
    """Функция-обработчик текста"""
    text = update.message.text
    if not re.match(POSITION_PATTERN, text):
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Нет действий с текстом: {text}"
        )
    result = re.search(POSITION_PATTERN, text)
    articul = result.group("articul")
    name = result.group("name")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Артикул: {articul}, название: {name}"
    )


async def unknown(update, context):
    """Функция-обработчик неизвестных боту команд."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=UNKNOWN_COMMAND_TEXT
    )


async def main_menu(update, context):
    """Функция-обработчик главного меню"""
    await context.bot.send_message(
        update.effective_chat.id,
        HELLO_MESSAGE,
        reply_markup=InlineKeyboardMarkup(main_keyboard)
    )


async def position_parser_info(update, context):
    """Функция-обработчик для кнопки Парсер позиций"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=POSITION_PARSER_MESSAGE,
        reply_markup=InlineKeyboardMarkup(parsing_keyboard_input)
    )


async def position_parser_expectations(update, context):
    """Функция-обработка запроса пользователя"""
    result = await position_parser(update)
    text_split = update.message.text.split()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=POSITION_PARSER_EXPECTATION_MESSAGE.format(
            text_split[0], ' '.join(text_split[1:])
        ),
        reply_markup=InlineKeyboardMarkup(parsing_keyboard_expectation),
        parse_mode='Markdown'
    )
    await position_parser_result(update, context, result)


async def position_parser_result(update, context, result):
    """Функция-вывод результата парсинга и кнопки Подписки(1/6/12ч)"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=POSITION_PARSER_RESULT_MESSAGE.format(result),
        reply_markup=InlineKeyboardMarkup(parsing_subscription_keyboard)
    )


async def send_position_parser_subscribe(update, context):
    """Функция-проверки подписки на периодичный парсинг (1/6/12ч)"""
    frequency = await position_parser_subscribe(update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=POSITION_PARSER_SUBSCRIBE_MESSAGE.format(frequency),
        reply_markup=InlineKeyboardMarkup(menu_keyboard)
    )


async def remainder_parser_info(update, context):
    """Функция-обработчик для кнопки Парсер остатков"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=LEFTOVERS_PARSER_MESSAGE,
        reply_markup=InlineKeyboardMarkup(leftovers_keyboard_input)
    )


async def remainder_parser_result(update, context):
    """Функция-вывода результатов парсинга по артикулу"""
    result = await remainder_parser(update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=LEFTOVERS_PARSER_RESULT_MESSAGE.format(result),
        reply_markup=InlineKeyboardMarkup(menu_keyboard)
    )


async def acceptance_rate_info(update, context):
    """Функция-обработчик для кнопки Отслеживание коэффицианта приемки WB"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ACCEPTANCE_RATE_MESSAGE,
    )


async def acceptance_rate_answer(update, context):
    """Функция-вывод результата Отслеживание коэффицианта приемки WB"""
    text = update.message.text
    if text in STOCS:
        result = await acceptance_rate_api(update)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ACCEPTANCE_RATE_ANSWER_MESSAGE.format(text, result),
        )
    else:
        await unknown(update, context)


async def get_subscriptions(update, context):
    """Функция-обработчик для кнопки Мои подписки на позиции"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=SUBSCRIPTIONS_MESSAGE,
        reply_markup=InlineKeyboardMarkup(menu_keyboard)
    )


def main():
    """Создаём в директории bot файл config.py и прописываем туда"""
    """bot_token = "ВАШ_ТОКЕН_ОТ_БОТА" """
    token = bot_token
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_bot_description())
    bot = Application.builder().token(token).build()
    logger.info("Бот успешно запущен.")
    bot.add_handler(CommandHandler('start', start))
    registration.registration_handlers(bot)
    bot.add_handler(CallbackQueryHandler(main_menu, pattern=MAIN_MENU))
    bot.add_handler(CommandHandler("stock", show_stock))
    bot.add_handler(CommandHandler("position", position))
    bot.add_handler(CallbackQueryHandler(check_callback))
    # bot.add_handler(MessageHandler(filters.TEXT, handle_cancel))
    # bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    bot.add_handler(MessageHandler(filters.COMMAND, unknown))
    bot.add_handler(
        MessageHandler(filters.Regex(r'^\d+$'), remainder_parser_result)
    )
    bot.add_handler(
        MessageHandler(
            filters.Regex(r'^\d+(\s\w*)*'), position_parser_expectations
        )
    )
    bot.add_handler(
        MessageHandler(filters.TEXT, acceptance_rate_answer)
    )
    bot.run_polling()


if __name__ == '__main__':
    main()
