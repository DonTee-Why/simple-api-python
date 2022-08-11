from redis import Redis
from datetime import timedelta
import os


redis_host = os.environ.get("REDIS_ENDPOINT_URI") or '127.0.0.1'
redis_password = os.environ.get("REDIS_PASSWORD") or ''
redis_db = os.environ.get("REDIS_DB") or 0
redis_port = os.environ.get("REDIS_PORT") or 6379

r = Redis(host=redis_host, password=redis_password, port=redis_port)
# r = Redis(host='127.0.0.1', port=6379, db=0)

def rate_limiter(key: str, limit: int, period: timedelta):
    """Limits the number of requests made by the user within a period of time.

    It uses the token bucket algorithm

    Parameters:
        r: Redis
            Redis client
        key: string
            Ip address of the user
        limit: int
            The number of requests allowed within a period of time
        period: timedelta
            The period of time a certain number of requests are allowed

    Returns:
        bool
    """
    if r.setnx(key, limit):
        r.expire(key, int(period.total_seconds()))
    user_record = r.get(key)
    
    if user_record and int(user_record) > 0:
        r.decrby(key, 1)
        return False
    else:
        return True