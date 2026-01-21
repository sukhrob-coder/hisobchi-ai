import redis

from .config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def set_linking_token(token: str, user_id: int):
    redis_client.setex(f"link:{token}", 300, str(user_id))

def get_user_id_by_token(token: str) -> str:
    return redis_client.get(f"link:{token}")

def delete_linking_token(token: str):
    redis_client.delete(f"link:{token}")

def store_temp_user_data(telegram_id: str, data: dict):
    redis_client.hmset(f"temp_user:{telegram_id}", data)
    redis_client.expire(f"temp_user:{telegram_id}", 3600)

def get_temp_user_data(telegram_id: str) -> dict:
    return redis_client.hgetall(f"temp_user:{telegram_id}")

def delete_temp_user_data(telegram_id: str):
    redis_client.delete(f"temp_user:{telegram_id}")
