from kombu import Exchange, Queue

BROKER_URL = 'redis://localhost:6379/3'  # 使用Redis作为消息代理

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # 把任务结果存在了Redis

CELERY_TASK_SERIALIZER = 'json'  # 任务序列化和反序列化使用msgpack方案

CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 任务过期时间

CELERY_ACCEPT_CONTENT = ['json', 'msgpack']  # 指定接受的内容类型

CELERY_QUEUE = (
    Queue("default", routing_key="task.#"),   # 路由键 以 "task." 开头的消息都进入 default 队列
    Queue("web_tasks", routing_key="web.#")   # 路由键 以 "web."开头的消息都进入 web_tasks 队列
)


CELERY_DEFAULT_EXCHANGE = "tasks"   # 默认交换机的名字为 tasks

CELERY_DEFAULT_EXCHANGE_KEY = "topic"   # 默认交换机的类型为 topic

CELERY_DEFAULT_ROUTING_KEY = "tasks.default"  # 默认的路由键是 task.default， 这个路由键符合上面的 default 队列

