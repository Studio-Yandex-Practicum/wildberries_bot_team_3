HELLO_MESSAGE = (
    "Добро пожаловать в No name Bot!\n"
    "Узнайте на каких позициях находится ваш товар в поиске Wildberries."
)
POSITION_PARSER_MESSAGE = (
    "Для определения позиции артикула отправьте сообщение в формате:\n"
    "Артикул Поисковая фраза\n"
    "Например:\n"
    "36704403 футболка женская"
)
POSITION_PARSER_EXPECTATION_MESSAGE = (
    "Запрос с артикулом *{}* и поисковой фразой "
    "*{}* поставлен в очередь на получение позиции"
)
POSITION_PARSER_RESULT_MESSAGE = "Результат запроса. Товар на {} месте"
LEFTOVERS_PARSER_MESSAGE = (
    "Отправьте артикул для вывода остатков:\n"
    "Например:\n"
    "36704403\n"
)
LEFTOVERS_PARSER_RESULT_MESSAGE = "остатки по складам и по размерам {}"
ACCEPTANCE_RATE_MESSAGE = "Выберите склад:\nНапример:\nАстрахань"
ACCEPTANCE_RATE_ANSWER_MESSAGE = (
    "Коэффицианта приемки для склада {} составляет {}"
)
SUBSCRIPTIONS_MESSAGE = "Вы подписаны на позиции: {}"
ERROR_MESSAGE = "Неизвестная команда, воспользуйтесь меню"