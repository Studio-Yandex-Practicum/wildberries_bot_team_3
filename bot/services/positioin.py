import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time


MAIN_URL = "https://www.wildberries.ru"


def prepare_phrase(phrase):
    """Заменяет все пробелы на "%20" для поисковой строки браузера"""
    return phrase.replace(" ", "%20")


def prepare_url(prepared_phrase):
    """Подготавливает поисковой запрос для браузера с подготовленной фразой"""
    url = urllib.parse.urljoin(
        MAIN_URL,
        '/catalog/0/search.aspx?search='
        + prepared_phrase
    )
    return url


def start_search(url):
    """Открываем браузер с переданной страницей для начала поиска """
    """и ждём 7 секунд для прогрузки страницы"""
    browser.get(url)
    time.sleep(7)


def get_full_page():
    while True:
        body = browser.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.END)
        time.sleep(2)
        if browser.execute_script(
            "return (window.innerHeight + window.scrollY) >= "
            "document.body.scrollHeight;"
         ):
            break


def palace_in_search(article):
    """Находит артикул на странице и возвращает его порядковый номер """
    """или None"""
    result = None
    my_good = None
    goods = browser.find_element(By.CLASS_NAME, 'product-card-list')
    goods_list = browser.find_elements(By.CSS_SELECTOR, 'article')

    try:
        my_good = goods.find_element(By.ID, f'c{article}')
    finally:
        if my_good:
            result = goods_list.index(my_good) + 1
        return result


def find_next_page_button():
    """Проверяет, есть ли кнопка перехода на следующую страницу"""
    """Если кнопка есть, то переходит по ссылке из неё"""
    try:
        element = browser.find_element(
            By.XPATH,
            '//a[contains(@class, "pagination-next pagination__next '
            'j-next-page") and contains(text(), "Следующая страница")]'
        )
        href = element.get_attribute("href")
        if href:
            browser.get(href)
            return True
    except NoSuchElementException:
        print("Кнопка следующей страницы не найдена.")
        return False


def prepare_result(place, page):
    """Возвращает отформатированный ответ"""
    result = (
        f"Ваш товар находится на {place} месте в выдаче страницы "
        f"номер {page}."
    )
    return result


def test_1():
    article = 154181703
    search_phrase = 'ветровка весенняя бомбер'
    expected_result = (
        'Ваш товар находится на 3 месте в выдаче страницы номер 3.'
    )
    result = full_search(search_phrase, article)
    print("Результат выполнения парсера: ", result)
    print("Ожидаемый результат теста: ", expected_result)
    assert result == expected_result


def test_2():
    article = 48605114
    search_phrase = 'жожа'
    expected_result = (
        'Ваш товар находится на 3 месте в выдаче страницы номер 1.'
    )
    result = full_search(search_phrase, article)
    print("Результат выполнения парсера: ", result)
    print("Ожидаемый результат теста: ", expected_result)
    assert result == expected_result


def test_3():
    article = 154181703
    search_phrase = 'жожа'
    expected_result = (
        "Артикул 154181703 по поисковому запросу 'жожа' не найден."
    )
    result = full_search(search_phrase, article)
    print("Результат выполнения парсера: ", result)
    print("Ожидаемый результат теста: ", expected_result)
    assert result == expected_result


def full_search(search_phrase, article):
    """Запуск полного цикла поиска"""
    prepared_phrase = prepare_phrase(search_phrase)
    url = prepare_url(prepared_phrase)

    start_search(url)
    page = 1

    while True:
        get_full_page()
        place = palace_in_search(article)
        if not place:
            next_page = find_next_page_button()
            if not next_page:
                return (
                    f"Артикул {article} по поисковому запросу "
                    f"'{search_phrase}' не найден."
                )
                break
            page += 1
            time.sleep(7)
        if place:
            break

    place = palace_in_search(article)
    if place:
        result = prepare_result(place, page)
        return result


def main():
    """Тесты раскоментить и запустить по одному за раз"""
    """Т.к позиции на wildberries постоянно меняются, то смотрим глазками)"""
    # test_1()
    test_2()
    # test_3()


if __name__ == '__main__':
    service = Service(executable_path='C:/chromedriver/chromedriver')
    browser = webdriver.Chrome(service=service)
    main()
