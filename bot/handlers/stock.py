from telegram import InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from constants import callback_data, commands, keyboards, messages, states
from handlers.menu import menu_callback
from services.stock import stock_parser


async def stock_callback(update, context):
    """Функция-обработчик для кнопки Парсер остатков."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.STOCK_MESSAGE,
        reply_markup=InlineKeyboardMarkup(keyboards.CANCEL_BUTTON)
    )
    return states.STOCK_RESULT


async def stock_result_callback(update, context):
    """Функция-вывода результатов парсинга по артикулу"""
    result = await stock_parser(update.message.text)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.STOCK_RESULT_MESSAGE.format(result),
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON)
    )
    return states.END


async def cancel_stock_callback(update, context):
    """Функция-обработчик для кнопки отмена."""
    await menu_callback(update, context, message=messages.CANCEL_MESSAGE)
    return states.END


stock_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(
            stock_callback,
            pattern=callback_data.GET_STOCK
        )],
        states={states.STOCK_RESULT: [MessageHandler(filters.Regex(r'^\d+$'),
                                                     stock_result_callback)]},
        fallbacks=[
            CallbackQueryHandler(
                cancel_stock_callback,
                pattern=callback_data.CANCEL_STOCK
            ),
            CommandHandler(commands.MENU, menu_callback),
            CommandHandler(commands.START, menu_callback),
        ],
        allow_reentry=True
    )


def stock_handlers(app):
    app.add_handler(stock_conv)
