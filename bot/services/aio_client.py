from aiohttp import ClientSession


async def get(url, data):
    async with ClientSession() as session:
        async with session.get(url=url, data=data) as response:
            data = await response.json()
            return data


async def post(url, data):
    async with ClientSession() as session:
        await session.post(url=url, data=data)


async def get_subscription(url):
    async with ClientSession() as session:
        async with session.get(url=url) as response:
            data = await response.json()
            return data


async def delete_subscription(url):
    async with ClientSession() as session:
        await session.delete(url=url)
