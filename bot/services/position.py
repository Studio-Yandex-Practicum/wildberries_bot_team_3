import time
import urllib.parse

from chromedriver_py import binary_path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


BROWSER_LOADING_TIME = 1
GEO_LOADING_TIME = 4
SCROLL_LOADING_TIME = 0.5

MAIN_URL = "https://www.wildberries.ru"
CITY = {
    "Санкт-Петербург": "Санкт-Петербург, метро Сенная площадь",
    "Москва": "Москва, метро Лубянка",
    "Казань": "г. Казань (Республика Татарстан)",
    "Краснодар": "Краснодар центр",
    "Екатеринбург": "Екатеринбург центр",
    "Владивосток": "город Владивосток",
}


def get_city(city):
    return CITY[city]


def prepare_url(search_phrase):
    """Подготавливает поисковой запрос для браузера"""

    url = urllib.parse.urljoin(
        MAIN_URL,
        '/catalog/0/search.aspx?search='
        + search_phrase
    )
    return url


def start_search(url, browser):
    """Открываем браузер с переданной страницей для начала поиска """
    """и ждём (BROWSER_LOADING_TIME = 7) секунд для прогрузки страницы"""
    browser.get(url)
    time.sleep(BROWSER_LOADING_TIME)


def prepare_city(city, browser):
    browser.get("https://www.wildberries.ru")
    time.sleep(BROWSER_LOADING_TIME)

    geo_city = browser.find_element(
        By.CLASS_NAME,
        "simple-menu__link.simple-menu__link--address."
        "j-geocity-link.j-wba-header-item"
    )

    geo_city.click()
    time.sleep(GEO_LOADING_TIME)

    search_input = browser.find_element(
        By.CLASS_NAME,
        "ymaps-2-1-79-searchbox-input__input"
    )
    search_input.send_keys(city)
    # time.sleep(1)
    search_input.send_keys(Keys.ENTER)
    time.sleep(BROWSER_LOADING_TIME)

    geo_list = browser.find_element(By.ID, "pooList")
    first_item = geo_list.find_element(
        By.CLASS_NAME,
        "address-item.j-poo-option"
    )
    first_item.click()
    time.sleep(BROWSER_LOADING_TIME)

    select_button = browser.find_element(
        By.XPATH,
        "//button[text()='Выбрать']"
    )
    select_button.click()
    time.sleep(BROWSER_LOADING_TIME)


def get_full_page(browser):
    """Проматывает страницу в самый низ, ожидая (SCROLL_LOADING_TIME = 2)"""
    """ секунды после каждой прокрутки для прогрузки скриптов"""
    while True:
        body = browser.find_element(By.TAG_NAME, "body")
        actions = ActionChains(browser)
        actions.move_to_element(body).send_keys(Keys.END).perform()
        time.sleep(SCROLL_LOADING_TIME)
        if browser.execute_script(
            "return (window.innerHeight + window.scrollY) >= "
            "document.body.scrollHeight;"
         ):
            break


def palace_in_search(article, browser):
    """Находит артикул на странице и возвращает его порядковый номер """
    """или None"""
    goods = browser.find_element(By.CLASS_NAME, 'product-card-list')
    goods_list = goods.find_elements(By.CSS_SELECTOR, 'article')
    articles = list(
        int(good.get_attribute('data-nm-id')) for good in goods_list
    )
    if article in articles:
        return goods_list.index(goods.find_element(By.ID, f'c{article}')) + 1


def find_next_page_button(browser):
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


def search(search_phrase, article, city, browser):
    """Запуск полного цикла поиска"""
    prepare_city(city, browser)
    url = prepare_url(search_phrase)

    start_search(url, browser)
    page = 1

    while True:
        get_full_page(browser)
        place = palace_in_search(article, browser)
        if not place:
            next_page = find_next_page_button(browser)
            if not next_page or page > 60:
                return (
                    f"Артикул {article} по поисковому запросу "
                    f"'{search_phrase}' не найден."
                )
                break
            page += 1
            time.sleep(BROWSER_LOADING_TIME)
        if place:
            break

    place = palace_in_search(article, browser)
    if place:
        result = prepare_result(place, page)
        return result


def full_search(search_phrase, article):
    for city_name in CITY:
        service = Service(executable_path=binary_path)
        chrome_options = Options()
        # chrome_options.add_argument("--headless") # для запуска без UI
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        browser = webdriver.Chrome(service=service, options=chrome_options)
        city = get_city(city_name)
        result = search(search_phrase, article, city, browser)
        browser.quit()
        return result
