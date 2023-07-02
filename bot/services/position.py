import time
import urllib.parse

from chromedriver_py import binary_path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


service = Service(executable_path=binary_path)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(service=service, options=options)

MAIN_URL = "https://www.wildberries.ru"
BROWSER_LOADING_TIME = 3
SCROLL_LOADING_TIME = 1

async def prepare_url(search_phrase):
    """Подготавливает поисковой запрос для браузера"""
    url = urllib.parse.urljoin(
        MAIN_URL,
        '/catalog/0/search.aspx?search='
        + search_phrase
    )
    return url


async def start_search(url):
    """Открываем браузер с переданной страницей для начала поиска """
    """и ждём (BROWSER_LOADING_TIME = 7) секунд для прогрузки страницы"""
    browser.get(url)
    time.sleep(BROWSER_LOADING_TIME)


async def get_full_page():
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


async def palace_in_search(article):
    """Находит артикул на странице и возвращает его порядковый номер """
    """или None"""
    goods = browser.find_element(By.CLASS_NAME, 'product-card-list')
    goods_list = goods.find_elements(By.CSS_SELECTOR, 'article')
    articles = list(
        int(good.get_attribute('data-nm-id')) for good in goods_list
    )
    if article in articles:
        return goods_list.index(goods.find_element(By.ID, f'c{article}')) + 1


async def find_next_page_button():
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


async def prepare_result(article, search_phrase, place, page):
    """Возвращает отформатированный ответ"""
    if page == 1:
        position = place
    else:
        position = page * 100 + place
    result = (
        f"Артикул: {article}\n"
        f"Запрос: {search_phrase}\n"
        f"Позиция: {position}\n"
        f"Ваш товар находится на {place} месте страницы номер {page}"
    )
    return result


async def full_search(search_phrase, article):
    """Запуск полного цикла поиска"""
    url = await prepare_url(search_phrase)

    await start_search(url)
    page = 1

    while True:
        await get_full_page()
        place = await palace_in_search(article)
        if not place:
            next_page = await find_next_page_button()
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

    place = await palace_in_search(article)
    if place:
        result = await prepare_result(article, search_phrase, place, page)
        return result
