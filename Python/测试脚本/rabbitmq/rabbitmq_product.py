import time
import pika
import json

user_info = pika.PlainCredentials("root", "root")  # 用户名密码
connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", 5672, "/", user_info))  # 连接上服务器的RabbitMQ服务

# 创建一个channel
channel = connection.channel()

# 如果指定的queue不存在，则会创建一个queue。如果已存在，则不会做其他动作，官方推荐，每次使用时可以加上这句
channel.queue_declare(queue="hello")

for i in range(0, 100):
    channel.basic_publish(exchange="",  # 当前是一个模式，所以这里设置为空字符串就可以了
                          routing_key="hello",  # 指定消息要发送到哪个queue
                          body=bytes(i)  # 指定要发送的消息
                          )
    time.sleep(1)

# 关闭连接
# connection.close()
