from aiohttp import ClientSession
from operator import itemgetter

from fastapi import HTTPException

from config import CMC_API_KEY
from routers.cache_operations import cache_coin, get_cached_coin


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
            result = await resp.json()
            if  resp.status == 200:
                crypto_data = result['data']
                key_to_sort = 'cmc_rank'
                sorted_crypto_data = sorted(crypto_data, key=itemgetter(key_to_sort))
                return {'data': sorted_crypto_data}
            else:
                return {"error": f"Failed to fetch data, status code: {resp.status}"}

class CoinRequest(HTTPClient):
    async def get_coin_data(self, id: int):
        async with self._session.get('/v2/cryptocurrency/quotes/latest',
                                     params={'id': id}) as resp:
            result = await resp.json()
            if resp.status == 200:
                return result['data'][str(id)]
            else:
                return {"error": f"Failed to fetch data, status code: {resp.status}"}

    async def get_coin_data_by_symbol(self, symbol: str):
            cached_data = get_cached_coin(symbol)
            if cached_data:
                return cached_data
            else:
                async with self._session.get('/v2/cryptocurrency/quotes/latest',
                                            params={'symbol': symbol}) as resp:
                    result = await resp.json()
                    if resp.status == 200:
                        data = result['data'][str(symbol)]
                        if result:
                            cache_coin(data, symbol)
                            return data
                        else:
                            raise HTTPException(status_code=500, detail="Error caching data")
                    else:
                        raise HTTPException(status_code= 503, detail=f"Failed to fetch data, status code: {resp.status}")


data_request = AllCoinsRequest(
    base_url= 'https://pro-api.coinmarketcap.com',
    api_key= f'{CMC_API_KEY}',
)
coin_data_request = CoinRequest(
    base_url= 'https://pro-api.coinmarketcap.com',
    api_key= f'{CMC_API_KEY}',
)