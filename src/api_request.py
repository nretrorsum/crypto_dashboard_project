from locale import currency

from aiohttp import ClientSession
import asyncio
import os

class HTTPClient:
    def __init__(self, base_url: str, api_key: str):
        self._session = ClientSession(
            base_url=base_url,
            headers={
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': api_key
            }
        )


#https://pro-api.coinmarketcap.com
class AllCoinsRequest(HTTPClient):
    async def get_data(self):
        async with self._session.get('/v1/cryptocurrency/listings/latest') as resp:
            result = await resp.json() # Отладочный вывод для проверки содержимого
            if resp.status == 200:
                return result['data']
            else:
                return {"error": f"Failed to fetch data, status code: {resp.status}"}

class CoinRequest(HTTPClient):
    async def get_coin_data(self, currency_id: int):
        async with self._session.get('/v2/cryptocurrency/quotes/latest',
                                     params={'id':currency_id}) as resp:
            result = await resp.json()
            if resp.status == 200:
                return result['data'][str(currency_id)]
            else:
                return {"error": f"Failed to fetch data, status code: {resp.status}"}
