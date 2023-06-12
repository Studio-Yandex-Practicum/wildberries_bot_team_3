import logging

from telegram import InlineKeyboardMarkup
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          MessageHandler, PicklePersistence, filters)

from config import bot_token
from constants import STOCS
from keyboards import (leftovers_keyboard_input, main_keyboard, menu_keyboard,
                       parsing_keyboard_expectation, parsing_keyboard_input,
                       parsing_subscription_keyboard)
from messages import (ACCEPTANCE_RATE_ANSWER_MESSAGE, ACCEPTANCE_RATE_MESSAGE,
                      ERROR_MESSAGE, HELLO_MESSAGE, LEFTOVERS_PARSER_MESSAGE,
                      LEFTOVERS_PARSER_RESULT_MESSAGE,
                      POSITION_PARSER_EXPECTATION_MESSAGE,
                      POSITION_PARSER_MESSAGE, POSITION_PARSER_RESULT_MESSAGE,
                      SUBSCRIPTIONS_MESSAGE)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


#  Привязка функций к кнопкам меню
async def check_callback_data(update, context):
    data = update.callback_query.data
    if data == 'main_menu':
        await wake_up(update, context)
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


#  Главное меню
async def wake_up(update, context):
    chat = update.effective_chat
    await context.bot.send_message(
        chat.id,
        HELLO_MESSAGE,
        reply_markup=InlineKeyboardMarkup(main_keyboard)
    )


#  Работа кнопки "Парсер позиций"
async def position_parser_info(update, context):
    # "Парсер позиций" Выводится пример запроса и кнопка "Отмена"
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=POSITION_PARSER_MESSAGE,
        reply_markup=InlineKeyboardMarkup(parsing_keyboard_input)
    )


async def position_parser_wildberrys(update, context):
    # Вызов парсера по артикулу и поисковой фразе (позиция в поиске)
    # Артикул и поисковая фраза товара для парсера:
    # text_split = update.message.text.split()
    # articul = text_split[0]
    # search_phrase = " ".join(text_split[1:])
    # Результат парсинга - позиция товара в поиске
    result = 33
    await position_parser_expectations(update, context)
    await position_parser_result(update, context, result)


async def position_parser_expectations(update, context):
    # "Парсер позиций" Выводится текст ожидания и кнопка "Отправить еще запрос"
    text_split = update.message.text.split()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=POSITION_PARSER_EXPECTATION_MESSAGE.format(
            text_split[0], " ".join(text_split[1:])
        ),
        reply_markup=InlineKeyboardMarkup(parsing_keyboard_expectation),
        parse_mode="Markdown"
    )


async def position_parser_result(update, context, result):
    # "Парсер позиций"
    # Вывод результата и кнопки Подписки(1/6/12ч) и Возврата в меню
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=POSITION_PARSER_RESULT_MESSAGE.format(result),
        reply_markup=InlineKeyboardMarkup(parsing_subscription_keyboard)
    )


#  Работа кнопки "Парсер остатков"
async def remainder_parser_info(update, context):
    # Кнопка "Парсер остатков" Выводится пример запроса и кнопка "Отмена"
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=LEFTOVERS_PARSER_MESSAGE,
        # Добавим кнопку в содержимое отправляемого сообщения
        reply_markup=InlineKeyboardMarkup(leftovers_keyboard_input)
    )


async def remainder_parser_wildberrys(update, context):
    # Вызов парсера по артикулу (остатки по складам и размерам)
    # Артикул товара для парсера articul = update.message.text
    # сообщение с результатами остатки по складам и по размерам.
    result = []
    await remainder_parser_result(update, context, result)


async def remainder_parser_result(update, context, result):
    # "Парсер остатков"
    # Выводится сообщение с результатами: остатки по складам и по размерам.
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=LEFTOVERS_PARSER_RESULT_MESSAGE.format(result),
        reply_markup=InlineKeyboardMarkup(menu_keyboard)
    )


#  Работа кнопки "Отслеживание коэффицианта приемки WB"
async def acceptance_rate_info(update, context):
    # Кнопка "Отслеживание коэффицианта приемки WB"
    # сообщение о фармате ввода склада
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ACCEPTANCE_RATE_MESSAGE,
    )


async def acceptance_rate_answer(update, context):
    # Кнопка "Отслеживание коэффицианта приемки WB"
    # проверка наличия склада из сообщения пользователя в списке складов
    text = update.message.text
    if text in STOCS:
        # Вызов функции для запроса коэффицианта приемки.
        # Результат запроса - коэффицианта приемки.
        result = 33
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


#  Работа кнопки "Мои подписки на позиции"
async def get_subscriptions(update, context):
    # Кнопка "Мои подписки на позиции" Запрос в БД для вывода подписок по id
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=SUBSCRIPTIONS_MESSAGE,
        reply_markup=InlineKeyboardMarkup(menu_keyboard)
    )


def main():
    """Создаём в директории bot файл config.py и прописываем туда """
    """bot_token = "ВАШ_ТОКЕН_ОТ_БОТА" """
    persistence = PicklePersistence(filepath="callbackdatabot")
    application = (
        Application.builder()
        .token(bot_token)
        .persistence(persistence)
        .arbitrary_callback_data(True)
        .build()
    )
    application.add_handler(CommandHandler('start', wake_up))
    application.add_handler(CallbackQueryHandler(check_callback_data))
    application.add_handler(
        MessageHandler(filters.Regex(r'^\d+$'), remainder_parser_wildberrys)
    )
    application.add_handler(
        MessageHandler(
            filters.Regex(r'^\d+(\s\w*)*'), position_parser_wildberrys
        )
    )
    application.add_handler(
        MessageHandler(filters.TEXT, acceptance_rate_answer)
    )
    application.run_polling()


if __name__ == '__main__':
    main()
