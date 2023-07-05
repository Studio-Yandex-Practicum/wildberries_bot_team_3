import re

import aiohttp
from constants import constant, messages

from . import aio_client, position


async def callback_alarm(context):
    user_id = context.job.data.get("user_id")
    articul = context.job.data.get("articul")
    try:
        subscribe_DB = await aio_client.get(
            constant.POSITION_SUBSCRIPTION_URL+"{}/{}".format(user_id, articul)
        )
        position_DB = subscribe_DB.get("position")
        result = position.full_search(
            context.job.data.get("text"), articul
        )
        position_in_parsing = re.search(
            constant.POSITION_IN_PARSING_RESULT_PATTERN, result
        )
        position_new = int(position_in_parsing.group(0).split()[1])
        await aio_client.patch(
            constant.POSITION_SUBSCRIPTION_URL+"{}/{}".format(
                user_id, articul
            ), data={"position": position_new}
        )
        change_of_position = position_DB - position_new
        if change_of_position > 0:
            text_change_of_position = f"+{change_of_position}"
        elif change_of_position > 0:
            text_change_of_position = f"-{change_of_position}"
        else:
            text_change_of_position = "0"
        await context.bot.send_message(
            chat_id=context.job.chat_id,
            text="{}\n{} {}".format(
                result,
                messages.PERIODIC_SUBSCRIBE_MESSAGE,
                text_change_of_position
            ))

    except aiohttp.ContentTypeError:
        context.job_queue.stop()


async def job(update, context, subscribe_data):
    chat_id = update.effective_chat.id
    frequency = subscribe_data.get("frequency")
    frequency_in_seconds = frequency*60*60
    await context.bot.send_message(
        chat_id=chat_id,
        text='Подписка активирована'
    )
    context.job_queue.run_repeating(
        callback_alarm,
        frequency_in_seconds,
        data=subscribe_data,
        chat_id=chat_id
    )
