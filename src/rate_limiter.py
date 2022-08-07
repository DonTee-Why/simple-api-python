from redis import Redis
from datetime import timedelta

def rate_limiter(r: Redis, key: str, limit: int, period: timedelta):
    """Limits the number of requests made by the user within a period of time.

    It uses the time bucket algorithm

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