import logging

from telegram import InlineKeyboardMarkup
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          MessageHandler, PicklePersistence, filters)

from constants.messages import (ACCEPTANCE_RATE_ANSWER_MESSAGE,
                                ACCEPTANCE_RATE_MESSAGE, ERROR_MESSAGE,
                                FALSE_SUBSCRIPTIONS_MESSAGE, HELLO_MESSAGE,
                                LEFTOVERS_PARSER_MESSAGE,
                                LEFTOVERS_PARSER_RESULT_MESSAGE,
                                POSITION_PARSER_EXPECTATION_MESSAGE,
                                POSITION_PARSER_MESSAGE,
                                POSITION_PARSER_RESULT_MESSAGE, START_MESSAGE,
                                SUBSCRIPTIONS_MESSAGE)
from constants.parser_constants import STOCS
from keyboards import (leftovers_keyboard_input, main_keyboard, menu_keyboard,
                       parsing_keyboard_expectation, parsing_keyboard_input,
                       parsing_subscription_keyboard, start_keyboard)
from services.services import (acceptance_rate_api, add_to_db, position_parser,
                               remainder_parser)
from settings import bot_token

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def check_callback(update, context):
    """Функция-обработчик callback запросов"""
    data = update.callback_query.data
    if data == 'main_menu':
        await start(update, context)
    if data == 'check_subscriptions':
        await check_subscriptions(update, context)
    if data == 'position_parser':
        await position_parser_info(update, context)
    elif data == 'remainder_parser':
        await remainder_parser_info(update, context)
    elif data == 'acceptance_rate':
        await acceptance_rate_info(update, context)
    elif data == 'position_subscriptions':
        await get_subscriptions(update, context)
    elif data == 'another_parsing_request':
        await position_parser_info(update, context)


async def start(update, context):
    """Функция-обработчик для команды /start"""
    await context.bot.send_message(
        update.effective_chat.id,
        START_MESSAGE,
        reply_markup=InlineKeyboardMarkup(start_keyboard)
    )


async def check_subscriptions(update, context):
    """Функция-проверки и внесения в БД нового подписчика"""
    if add_to_db(update):
        await wake_up(update, context)
    else:
        await context.bot.send_message(
            update.effective_chat.id,
            FALSE_SUBSCRIPTIONS_MESSAGE,
        )
        await start(update, context)


async def wake_up(update, context):
    """Функция-обработчик для команды /start"""
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
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ERROR_MESSAGE,
            reply_markup=InlineKeyboardMarkup(menu_keyboard)
        )


async def get_subscriptions(update, context):
    """Функция-обработчик для кнопки Мои подписки на позиции"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=SUBSCRIPTIONS_MESSAGE,
        reply_markup=InlineKeyboardMarkup(menu_keyboard)
    )


def main():
    persistence = PicklePersistence(filepath='callbackdatabot')
    application = (
        Application.builder()
        .token(bot_token)
        .persistence(persistence)
        .arbitrary_callback_data(True)
        .build()
    )
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(check_callback))
    application.add_handler(
        MessageHandler(filters.Regex(r'^\d+$'), remainder_parser_result)
    )
    application.add_handler(
        MessageHandler(
            filters.Regex(r'^\d+(\s\w*)*'), position_parser_expectations
        )
    )
    application.add_handler(
        MessageHandler(filters.TEXT, acceptance_rate_answer)
    )
    application.run_polling()


if __name__ == '__main__':
    main()
