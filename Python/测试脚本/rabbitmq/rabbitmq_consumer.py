import time
import pika
import json

user_info = pika.PlainCredentials("root", "root")  # 用户名密码
connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", 5672, "/", user_info))  # 连接上服务器的RabbitMQ服务

# 创建一个channel
channel = connection.channel()

# 如果指定的queue不存在，则会创建一个queue。如果已存在，则不会做其他动作，官方推荐，每次使用时可以加上这句
channel.queue_declare(queue="hello")


# 回调函数
def callback(ch, method, properties, body):
    print(f"消费者收到: {body}")


channel.basic_consume(queue="hello",  # 指定queue的消息
                      auto_ack=True,  # 指定为True，表示接收到消息后，自动给消息发送方回复确认， 已收到消息
                      on_message_callback=callback  # 指定要发送的消息
                      )

print("waiting for messages. To exit press CTRL+C")

# 一直处于等待接收消息的状态，如果没接到消息就一直处于阻塞状态，收到消息就调用上面的回调函数
channel.start_consuming()
