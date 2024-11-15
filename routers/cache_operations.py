from typing import Optional
import redis
from routers.schemas import ReadUser
from config import REDIS_HOST, REDIS_PORT
from uuid import UUID

redis_client = redis.Redis(host=f'{REDIS_HOST}', port=f'{REDIS_PORT}', db=0)

def cache_user(user_id: UUID, user_data: ReadUser):
    redis_client.set(f'user: {user_id}', user_data.json(), ex=3600)

def get_cached_user(user_id: UUID) -> Optional[ReadUser]:
    cached_user = redis_client.get(f'user:{user_id}')
    if cached_user:
        return ReadUser.parse_raw(cached_user)
    return None

def cache_currencies(data: str):
    redis_client.set('crypto_data', str(data), ex=3600)

def get_cached_cryptodata():
    cached_cryptodata = redis_client.get('crypto_data')
    if cached_cryptodata:
        return eval(cached_cryptodata)
    return None

def cache_coin(data: str, ticker: str):
    redis_client.set(f'coin:{ticker}', str(data), ex=3600)

def get_cached_coin(ticker: str):
    cached_coin = redis_client.get(f'coin:{ticker}')
    if cached_coin:
        return eval(cached_coin)
    return None