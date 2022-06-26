from __future__ import print_function
from __future__ import unicode_literals
from prompt_toolkit import *
from prompt_toolkit.history import FileHistory  # 保存历史命令
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory  # 从历史记录中自动提示命令
from prompt_toolkit.contrib.completers import *

import json
import threading
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

client: mqtt.Client

# 全局变量
cloud_rsp_msg = {}
subscribe_topic = "test"  # 订阅的topic
register_code = ""

BaseCompleter = SystemCompleter()  # 系统指令自动补全


def on_message_callback(client, userdata, message):
    # logger.info(message.topic + " " + ":" + str(message.payload))
    cloud_msg = json.loads(str(message.payload.decode('utf-8')))
    cloud_rsp_msg[cloud_msg["requestId"]] = cloud_msg
    logger.info(f"cloud_msg: {cloud_rsp_msg}")
    # logger.info(message.topic + " " + ":" + str(message.payload))


def on_connect(client, userdata, flags, rc):
    global subscribe_topic
    logger.info("Connected with result code " + str(rc))
    client.subscribe(subscribe_topic)


def get_uuid() -> str:
    return str(uuid.uuid1()).replace("-", "")


# {"requestId": "bfa6557fe3674256b2d2efc411a6cad1"}


def send_thread():
    global client
    global cloud_rsp_msg
    global register_code
    time.sleep(3)
    if client.is_connected():
        logger.info("连接成功")
        # logger.info("请输入需要发送的topic：")
        # publish_topic = input("请输入需要发送的topic：")
        publish_topic = f"$kibo/ids/p2p/{register_code}/cloud/req"

        while True:
            # send_msg = input("请输入需要发送的消息：")
            send_msg = prompt(u'>> ', history=FileHistory("../../remote_debug/test/history.txt"),
                              auto_suggest=AutoSuggestFromHistory(), completer=BaseCompleter)
            # 如果输入 exit， 则退出
            if send_msg.strip().lower() == "exit":
                break
            rc, mid = client.publish(publish_topic, send_msg, 1)
            logger.info("发送： {} 成功 ".format(send_msg))
            send_msg = json.loads(send_msg)
            if rc == 0:
                receive_data = {}
                for i in range(30):
                    receive_data = cloud_rsp_msg.get(send_msg["requestId"])
                    if receive_data:
                        logger.info('cloud rsp: {}'.format(receive_data))
                        del cloud_rsp_msg[send_msg["requestId"]]
                        break
                    time.sleep(1)
                if not receive_data:
                    logger.info("超时未响应")
    else:
        logger.warning("连接失败")


def main():
    global client
    client = mqtt.Client('client_id_send')
    client.connect(HOST, PORT, 60)
    client.tls_set(ca_certs=MQTT_CA, certfile=MQTT_CERT, keyfile=MQTT_KEY,
                   cert_reqs=ssl.CERT_NONE)
    client.username_pw_set('kibo-swift-term', 'kiboterm@2020')
    client.on_connect = on_connect
    # client.publish("xhjtestsend", "666666666", 1)
    # client.subscribe('gg')
    client.on_message = on_message_callback
    client.loop_forever()


if __name__ == '__main__':
    register_code = input("请输入注册码： ")
    # subscribe_topic = input("请输入需要订阅的topic")
    subscribe_topic = f"$kibo/ids/p2p/{register_code}/device/rsp"
    threading.Thread(target=send_thread).start()
    main()
