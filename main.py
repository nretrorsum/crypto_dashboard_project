from http.client import HTTPException
from fastapi import FastAPI, HTTPException
from api_processing.news_processing import news_api_processing
from app_functions.investment import Investment
from auth.auth import auth_router
from database.repository import repository
from routers.user_routers import user_router
import redis
import json
from api_processing.api_request import data_request, coin_data_request

app = FastAPI()
investment = Investment(repository, coin_data_request)

redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)

app.include_router(
    user_router,
    prefix="/users",
    tags=["Users"]
)


@app.get("/coin/{id}")
async def get_coin(id: int):
    data = await coin_data_request.get_coin_data(id)
    if "error" in data:
        return {"status": "failed", "message": data["error"]}
    return {"status": "success", "data": data}

@app.get("/news/{currency_name}")
async def app_get_news(currency_name: str):
    data = await news_api_processing.get_news(currency_name)
    result = data['articles'][:3]

    return {"status": "success", "data": result}

@app.post('/cache_currency_list', status_code=201)
async def cache_currency_list():
    data = await data_request.get_data()
    json_data= json.dumps(data)
    redis_client.setex("cryptocurrencies", 3600, json_data)
    return {'status': 'Data cached'}

@app.get('/get_currencies', status_code=200)
async def get_currencies():
    data = redis_client.get("cryptocurrencies")
    if data:
        return json.loads(data)
    raise HTTPException(status_code=404, detail="No data found")

@app.get('/get_profit/{user_id}/{portfolio_id}', status_code=200)
async def get_profit(user_id: int, portfolio_id: int):
    performance_data = await investment.calculate_portfolio_performance(user_id, portfolio_id)
    return {"status": "success", "data": performance_data}
