from httpx import AsyncClient
from config import NEWS_API_KEY


class GetNews:
    def __init__(self, _api_key):
        self._api_key = _api_key
        print(self._api_key)

    async def get_api_key(self):
        return self._api_key

    async def get_news(self, key_arg: str):
        async with AsyncClient() as client:
            headers = {
                'X-Api-Key': await self.get_api_key()
            }
            response = await client.get(f'https://newsapi.org/v2/everything?q={key_arg}', headers=headers)
            if response.status_code == 200:
                   return response.json()
            else:
                return {'error': response.text}


news_api_processing = GetNews(NEWS_API_KEY)

