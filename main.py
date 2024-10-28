from fastapi import FastAPI
from src.api_request import AllCoinsRequest, CoinRequest

app = FastAPI()

data_request = AllCoinsRequest(
    base_url= 'https://pro-api.coinmarketcap.com',
    api_key= '05833a2e-b625-4957-9ca8-dc63b304df8e'
)
coin_data_request = CoinRequest(
    base_url= 'https://pro-api.coinmarketcap.com',
    api_key= '05833a2e-b625-4957-9ca8-dc63b304df8e'
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