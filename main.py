from fastapi import FastAPI
from api_processing.api_request import AllCoinsRequest, CoinRequest
from api_processing.news_processing import news_api_processing
from auth.auth import auth_router
from routers.user_routers import user_router
from config import CMC_API_KEY

app = FastAPI()
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



data_request = AllCoinsRequest(
    base_url= 'https://pro-api.coinmarketcap.com',
    api_key= f'{CMC_API_KEY}',
)
coin_data_request = CoinRequest(
    base_url= 'https://pro-api.coinmarketcap.com',
    api_key= f'{CMC_API_KEY}',
)
@app.get("/currencies")
async def get_currencies():
    data = await data_request.get_data()
    if "error" in data:
        return {"status": "failed", "message": data["error"]}
    return {"status": "success", "data": data}

@app.get("/coin/{id}")
async def get_coin(id: int):
    data = await coin_data_request.get_coin_data(id)
    if "error" in data:
        return {"status": "failed", "message": data["error"]}
    return {"status": "success", "data": data}

@app.get("/news/{currency_name}")
async def app_get_news(currency_name: str):
    result = await news_api_processing.get_news(currency_name)

    return {"status": "success", "data": result}