import redis

pool = redis.ConnectionPool(host="localhost", port=6379, decode_responses=True)

redis_conn = redis.Redis(connection_pool=pool)


