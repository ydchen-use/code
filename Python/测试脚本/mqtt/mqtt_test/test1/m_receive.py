import datetime
import time
import uuid
import ssl

import paho.mqtt.client as mqtt
from loguru import logger

HOST = "192.168.20.50"
PORT = 8883  # 端口
# 以下是证书路径
MQTT_CA = "my_root_ca.pem"
MQTT_CERT = "client.pem"
MQTT_KEY = "client.key"


def on_message_callback(client, userdata, message):
    logger.info({"topic": message.topic, "now_time": str(datetime.datetime.now()), "msg": str(message.payload)})


def on_connect(client, userdata, flags, rc):
    global subscribe_topic
    logger.info("Connected with result code " + str(rc))
    client.subscribe(subscribe_topic)


def get_uuid() -> str:
    return str(uuid.uuid1()).replace("-", "")


def mqtt_receive(topic: str):
    """
    订阅消息
    :param topic: 
    :return: 
    """
    client = mqtt.Client('client_id_receive')
    client.connect(HOST, PORT, 60)
    client.tls_set(ca_certs=MQTT_CA, certfile=MQTT_CERT, keyfile=MQTT_KEY,
                   cert_reqs=ssl.CERT_NONE)
    client.username_pw_set('kibo-swift-term', 'kiboterm@2020')
    client.on_connect = on_connect
    # client.publish("xhjtest", "666666666", 1)
    # client.subscribe('gg')
    client.on_message = on_message_callback
    client.loop_forever()


if __name__ == '__main__':
    subscribe_topic = input("请输入需要订阅的topic")
    mqtt_receive(subscribe_topic)
