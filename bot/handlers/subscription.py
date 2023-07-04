import re

from telegram import InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler)

from constants import (callback_data, commands, constant, keyboards, messages,
                       states)
from handlers.menu import menu_callback
from services import aio_client


async def subscription_callback(update, context):
    """Функция-обработчик для кнопки Мои подописки."""
    user_id = int(update.callback_query.from_user.id)
    subscription = await aio_client.get_subscription(
        constant.POSITION_SUBSCRIPTION_URL+"{}".format(user_id)
    )
    if not len(subscription):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=messages.EMPTY_SUBSCRIBE_MESSAGE,
            reply_markup=InlineKeyboardMarkup(
                keyboards.UNSUBSCRIBE_CANCEL_BUTTON
            )
        )
        return states.END
    for _ in subscription:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=messages.SUBSCRIBE_MESSAGE.format(
                _.get("articul"), _.get("text"), _.get("frequency")
            ),
            reply_markup=InlineKeyboardMarkup(keyboards.UNSUBSCRIBE_BUTTON)
        )
    return states.UNSUBSCRIBE


async def unsubscription_callback(update, context):
    """Функция-обработчик для кнопки Мои подописки."""
    user_id = int(update.callback_query.from_user.id)
    subscription = update.callback_query.message.text
    articul_pfrase = re.search(
        constant.ARTICUL_IN_PARSING_RESULT_PATTERN, subscription
    )
    articul = int(articul_pfrase.group(0).split()[1])
    constant.ARTICUL_IN_PARSING_RESULT_PATTERN
    await aio_client.delete_subscription(
        constant.POSITION_SUBSCRIPTION_URL+"{}/{}".format(user_id, articul)
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.UNSUBSCRIBE_MESSAGE.format(subscription),
        reply_markup=InlineKeyboardMarkup(keyboards.UNSUBSCRIBE_CANCEL_BUTTON),
        parse_mode="Markdown"
    )
    return states.UNSUBSCRIBE


async def cancel_subscribe_callback(update, context):
    """Функция-обработчик для кнопки отмена."""
    await menu_callback(update, context, message=messages.CANCEL_MESSAGE)
    return states.END


subscribe_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(
            subscription_callback,
            pattern=callback_data.GET_POSITION_SUBSCRIPTIONS
        )],
        states={
            states.UNSUBSCRIBE: [
                CallbackQueryHandler(
                    unsubscription_callback,
                    pattern=callback_data.UNSUBSCRIBE
                ),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(
                cancel_subscribe_callback,
                pattern=callback_data.CANCEL_UNSUBSCRIBE
            ),
            CommandHandler(commands.MENU, menu_callback),
            CommandHandler(commands.START, menu_callback),
        ],
        allow_reentry=True
    )


def subscription_handlers(app):
    app.add_handler(subscribe_conv)
