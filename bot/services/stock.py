import asyncio

import aiohttp

from aio_client import post


async def prepare_params(article, session):
    """Делаем запрос к API wildberries для подготовки параметров"""
    """Добавляем наш артикул к параметрам запроса"""
    url = 'https://user-geo-data.wildberries.ru/get-geo-info'
    async with session.get(url) as response:
        json_data = await response.json()
        params = {
            param.split('=')[0]: param.split('=')[1] for param
            in json_data['xinfo'].split('&')
        }
        params['nm'] = article
        return params


async def get_json(url, params, session):
    """Делаем асинхронный запрос на переданный url с переданными параметрами"""
    """Получаем json и возвращаем его"""
    async with session.get(url, params=params) as response:
        json_data = await response.json()
        return json_data


def parse_json(json):
    """Парсим json, достаём необходимые данные, приводим к читаемому виду"""
    sizes_list = []
    stocks_list = []
    for size in json['data']['products'][0]['sizes']:
        if size['stocks']:
            stocks_list = [
                {
                    'ID Склада': item['wh'],
                    'Количество': item['qty']
                } for item in size['stocks']
            ]
            sizes_list.append({
                'Название': size['name'],
                'Обозначение': size['origName'],
                'Склады': stocks_list,
            })
    return sizes_list


async def main(article):
    """Парочка тестовых данных, нужно раскоментить"""
    """лучше по одному за раз, чтоб всё не смешалось в кучу"""

    # article = 145057465
    # article = 155164499
    # article = 110727236
    url = 'https://card.wb.ru/cards/detail'

    await post('http://127.0.0.1:5000/api/request_stock/',
               {"articul": article})

    async with aiohttp.ClientSession() as session:
        params = await prepare_params(article, session)
        json_data = await get_json(url, params, session)
        return parse_json(json_data)


def stock_parser(article):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(article))
