import asyncio
from aiohttp import ClientSession


class OpenGraph:

    DEFAULT_FIELDS = ['title', 'type', 'image', 'url', 'description']

    def __init__(self, urls, fields=None):
        """
        :type urls: list/set
        :type fields: list
        """
        self.urls = urls
        self.fields = fields if fields else self.DEFAULT_FIELDS

    async def fetch(self, url, session):
        async with session.get(url) as response:
            return await response.read()

    async def fetch_urls(self):
        tasks = []

        # Fetch all responses within one Client session,
        # keep connection alive for all requests.
        async with ClientSession() as session:
            for url in self.urls:
                task = asyncio.ensure_future(self.fetch(url, session))
                tasks.append(task)

            responses = await asyncio.gather(*tasks)
            return responses
