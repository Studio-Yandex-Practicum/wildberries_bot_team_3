import re

POSITION_MESSAGE = (
    "Для определения позиции артикула отправьте сообщение в формате\n"
    "'Артикул Поисковая фраза'\n\n"
    "Например:\n36704403 футболка женская"
)

UNKNOWN_COMMAND_TEXT = "Я пока не знаю такой команды."
POSITION_PATTERN = re.compile(r"^(?P<articul>\d*)\s(?P<name>.*)")
