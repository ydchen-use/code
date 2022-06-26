import threading
import time
import redis

from redis import StrictRedis


class RedisLock(object):
    def __init__(self, redis_conn):
        self.redis_conn = redis_conn

    def get_lock_key(self, key):
        lock_key = 'lock_%s' % key
        return lock_key

    def get_lock(self, key):
        lock_key = self.get_lock_key(key)
        while True:
            value = self.redis_conn.get(lock_key)
            if not value:
                self.redis_conn.set(lock_key, 1)
                return True
            time.sleep(0.01)

    def del_lock(self, key):
        lock_key = self.get_lock_key(key)
        return self.redis_conn.delete(lock_key)


def increase_data(redis_conn, lock, key):
    lock_value = lock.get_lock(key)  # 获取锁
    value = redis_conn.get(key)  # 获取数据
    time.sleep(0.1)
    if value:
        value = int(value) + 1
    else:
        value = 0
    redis_conn.set(key, value)
    thread_name = threading.current_thread().name
    print(thread_name, value)
    print("\n")
    lock.del_lock(key)  # 释放锁


##主程序
if __name__ == "__main__":
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=8)
    redis = StrictRedis(connection_pool=pool)
    lock = RedisLock(redis)
    key = 'test_key'
    thread_count = 10
    redis.delete(key)
    for i in range(thread_count):
        thread = threading.Thread(target=increase_data, args=(redis, lock, key))
        thread.start()
