from typing import Optional
import redis
from routers.schemas import ReadUser

redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)

def cache_user(user_id: int, user_data: ReadUser):
    redis_client.set(f'user: {user_id}', user_data.json(), ex=3600)

def get_cached_user(user_id: int) -> Optional[ReadUser]:
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