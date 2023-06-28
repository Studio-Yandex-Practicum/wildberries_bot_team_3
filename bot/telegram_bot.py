import asyncio
import logging

import aiohttp
from telegram import InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler,
                          MessageHandler, filters)
from telegram.ext import Application, CommandHandler

from config import bot_token
from constants.buttons import MAIN_MENU, subscribe_message
from constants.messages import (ACCEPTANCE_RATE_MESSAGE, HELLO_MESSAGE,
                                LEFTOVERS_PARSER_MESSAGE,
                                POSITION_PARSER_EXPECTATION_MESSAGE,
                                POSITION_PARSER_MESSAGE,
                                POSITION_PARSER_RESULT_MESSAGE,
                                POSITION_PARSER_SUBSCRIBE_MESSAGE,
                                START_MESSAGE, SUBSCRIPTIONS_MESSAGE,
                                START_BOT_DESCRIPTION_MESSAGE)
from handlers import menu, rate, registration, position, stock
from keyboards import (leftovers_keyboard_input, main_keyboard, menu_keyboard,
                       parsing_keyboard_expectation, parsing_keyboard_input,
                       parsing_subscription_keyboard)
from services.services import position_parser, position_parser_subscribe


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


async def handle_cancel(update, context):
    """Функция-обработчик для нажатия на кнопку 'Отмена'"""
    message_text = update.message.text
    if message_text == 'Отмена':
        cancel_message = 'Действие отменено'
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=cancel_message
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


async def acceptance_rate_info(update, context):
    """Функция-обработчик для кнопки Отслеживание коэффицианта приемки WB"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ACCEPTANCE_RATE_MESSAGE,
    )


async def get_subscriptions(update, context):
    """Функция-обработчик для кнопки Мои подписки на позиции"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=SUBSCRIPTIONS_MESSAGE,
        reply_markup=InlineKeyboardMarkup(menu_keyboard)
    )


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_bot_description())
    bot = Application.builder().token(bot_token).build()
    logger.info('Бот успешно запущен.')
    bot.add_handler(CommandHandler('start', start))
    registration.registration_handlers(bot)
    menu.menu_handlers(bot)
    position.position_handlers(bot)
    stock.stock_handlers(bot)
    rate.rate_handlers(bot)
    bot.add_handler(
        MessageHandler(
            filters.Regex(r'^\d+(\s\w*)*'), position_parser_expectations
        )
    )
    bot.run_polling()


if __name__ == '__main__':
    main()
