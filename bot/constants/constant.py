COMMAND_NAME = '@...'
BOT_NAME = 'No name Bot'
TELEGRAM_CHANEL_SUBSCRIBE = 'https://t.me/dbfsfg'
URL = '176.53.162.80'
REQUEST_POSITION_URL = 'http://{}/api/request_position/'.format(URL)
POSITION_SUBSCRIPTION_URL = 'http://{}/api/position_subscription/'.format(URL)
POSITION_PATTERN = r"^(?P<articul>\d+)(?P<phrase>(\s+[a-zA-Zа-яА-ЯёЁ]+)+)"
SUBSCRIPTION_PATTERN = r"(?P<articul>^\d+)"
ARTICUL_IN_PARSING_RESULT_PATTERN = r"\Артикул: \d+"
TEXT_IN_PARSING_RESULT_PATTERN = r"\Запрос: \w+"
POSITION_IN_PARSING_RESULT_PATTERN = r"\Позиция: \d+"

# После получения доступа к каналу подписки с правами админа
# TELEGRAM_CHANEL_SUBSCRIBE = 'https://t.me/mpexperts'
