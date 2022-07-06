import redis
import uuid
import math
import time

from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# redis连接
redis_client = redis.Redis(host="127.0.0.1",
                           port=6379,
                           db=8)


def acquire_lock_with_timeout(conn, lock_name, acquire_timeout=10, lock_timeout=10):
    """
    基于 Redis 实现的分布式锁

    :param conn: Redis 连接
    :param lock_name: 锁的名称
    :param acquire_timeout: 获取锁的超时时间，默认 3 秒
    :param lock_timeout: 锁的超时时间，默认 2 秒
    :return:
    """

    identifier = str(uuid.uuid4())
    lockname = f'lock:{lock_name}'
    lock_timeout = int(math.ceil(lock_timeout))

    end = time.time() + acquire_timeout

    while time.time() < end:
        # 如果不存在这个锁则加锁并设置过期时间，避免死锁
        if conn.setnx(lockname, identifier):
            # 给锁设置超时时间, 防止进程崩溃导致其他进程无法获取锁
            redis_client.expire(lockname, lock_timeout)
            return identifier
        elif not redis_client.ttl(lockname):
            redis_client.expire(lockname, lock_timeout)

        time.sleep(0.001)

    return False


def release_lock(conn, lock_name, identifier):
    """
    释放锁

    :param conn: Redis 连接
    :param lockname: 锁的名称
    :param identifier: 锁的标识
    :return:
    """
    unlock_script = """
    if redis.call("get",KEYS[1]) == ARGV[1] then
        return redis.call("del",KEYS[1])
    else
        return 0
    end
    """
    lockname = f'lock:{lock_name}'
    unlock = conn.register_script(unlock_script)
    result = unlock(keys=[lockname], args=[identifier])
    if result:
        return True
    else:
        return False


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/add_post", methods=["POST"])
def add_post():
    print(request.headers)
    print(type(request.json))
    print(request.json)
    result = request.json
    return str(result)


if __name__ == "__main__":
    while True:
        # 获取锁
        identifier = acquire_lock_with_timeout(redis_client, "lock_distribute")
        # 如果获得锁了
        if identifier:
            print(f"get lock {identifier}")
            app.run(debug=False)
            time.sleep(10)
        else:
            print("not get lock, please wait...")
            time.sleep(60)
