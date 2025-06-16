import redis
import json

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def get_cache(key: str):
    data = r.get(key)
    return json.loads(data) if data else None


def set_cache(key: str, value, expire_seconds: int = 600):
    r.set(key, json.dumps(value), ex=expire_seconds)
