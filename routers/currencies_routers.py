from fastapi import APIRouter

from api_processing.api_request import coin_data_request, data_request
from api_processing.news_processing import news_api_processing
from routers.cache_operations import get_cached_cryptodata, cache_currencies

currency_router = APIRouter()

@currency_router.get("/coin/{id}")
async def get_coin(id: int):
    data = await coin_data_request.get_coin_data(id)
    if "error" in data:
        return {"status": "failed", "message": data["error"]}
    return {"status": "success", "data": data}

@currency_router.get("/news/{currency_name}")
async def app_get_news(currency_name: str):
    data = await news_api_processing.get_news(currency_name)
    result = data['articles'][:3]

    return {"status": "success", "data": result}

@currency_router.get('/cached_currency_list', status_code=200)
async def cache_currency_list():
    cached_data = get_cached_cryptodata()
    if cached_data:
        return {"status": "success", "data": cached_data}

    data = await data_request.get_data()
    if data:
        cache_currencies(data)
        return {"status": "success", "data": data}