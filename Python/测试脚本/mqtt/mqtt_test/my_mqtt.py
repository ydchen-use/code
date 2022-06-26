import json
import threading
import time
import uuid
import ssl
import hashlib

import paho.mqtt.client as mqtt
from loguru import logger

HOST = "192.168.20.50"
# HOST = "in.aiot.swiftsec.com.cn"
PORT = 8883  # 端口
ACCOUNT = "kibo-swift-term"
PASSWORD = "kiboterm@2020"

# 以下是证书路径
MQTT_CA = "mqtt_config/my_root_ca.pem"
MQTT_CERT = "mqtt_config/client.pem"
MQTT_KEY = "mqtt_config/client.key"

# 全局变量
cloud_rsp_msg = {}
publish_topic = "test"  # 发布的topic
subscribe_topic = "test"  # 订阅的topic
register_code = ""  # 注册码

# 裸命令
nonce = str(uuid.uuid4())
SECRET = 'KIBOIDS@3vFUvY8kV89}p;msSWORDFISH$_~{}CMD'

# MQTT连接
client: mqtt.Client

data = {
    "methodName": "reqRequireNetcardStatus",
    "requestId": "aa703d50-7ed7-48db-9d01-1662e6c6018b",
    "payload": {}
}

data1 = {
    "test": "test",
    "data": 1
}


def on_message_callback(client, userdata, message):
    logger.info(message.topic + " " + str(message.payload))
    cloud_msg = json.loads(str(message.payload.decode('utf-8')))
    cloud_rsp_msg[cloud_msg["requestId"]] = cloud_msg
    logger.info(f"cloud_msg: {cloud_rsp_msg}")


# 当代理响应订阅请求时被调用
def on_subscribe(client, userdata, mid, granted_qos):
    global subscribe_topic
    client.subscribe(subscribe_topic)
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# 当使用publish发送的消息已经传输到代理时被调用
def on_publish(client, obj, mid):
    print("OnPublish, mid: " + str(mid))


def on_connect(client, userdata, flags, rc):
    global subscribe_topic
    logger.info("Connected with result code " + str(rc))
    client.subscribe(subscribe_topic)


def on_disconnect(client, userdata, rc):
    mqtt_is_connected = False
    logger.warning("mqtt disconnected!")


def on_command_message(client, userdata, msg):
    print("on_command_message 主题:" + msg.topic + " 消息:" + str(msg.payload.decode('utf-8')))


def get_uuid() -> str:
    return str(uuid.uuid1()).replace("-", "")


def send_message(send_msg):
    global client
    global cloud_rsp_msg
    global register_code
    global publish_topic

    try:
        rc, mid = client.publish(publish_topic, send_msg, 1)
        logger.info("发送： {} 成功 ".format(send_msg))
        send_msg = json.loads(send_msg)
        # 轮询检查是否有返回， 30s无返回则超时
        if rc == 0:
            receive_data = {}
            for i in range(30):
                receive_data = cloud_rsp_msg.get(send_msg["requestId"])
                if receive_data:
                    if receive_data["methodName"] == "reqRawCmd":
                        cloud_msg = receive_data["data"]
                        print("args:" + f"{cloud_msg['args']}" + "\n")
                        print("code:" + f"{cloud_msg['code']}" + "\n")
                        print("stdout:" + f"{cloud_msg['stdout']}" + "\n")
                        print("stderr:" + f"{cloud_msg['stderr']}")
                    else:
                        print('cloud rsp: {}'.format(receive_data["data"]))
                    del cloud_rsp_msg[send_msg["requestId"]]
                    break
                time.sleep(1)
            if not receive_data:
                logger.info("超时未响应")
    except:
        pass


def get_registration_code_topic():
    """
    获取 注册码
    mqtt topic
    :return:
    """
    global register_code
    global subscribe_topic
    global publish_topic

    register_code = input("请输入注册码：").strip()  # 注册码
    if register_code == "exit":
        pass
    else:
        subscribe_topic = f"$kibo/ids/p2p/+/device/rsp"  # 订阅的topic
        publish_topic = f"$kibo/ids/p2p/{register_code}/cloud/req"  # 发布的topic
        # subscribe_topic = "test"
        # publish_topic = "test"


def mqtt_connect_main():
    """
    MQTT连接主函数
    :return:
    """
    global client

    # 获取client_id
    client_id = get_uuid()

    client = mqtt.Client(client_id)
    client.connect(HOST, PORT, 60)
    client.tls_set(ca_certs=MQTT_CA, certfile=MQTT_CERT, keyfile=MQTT_KEY, cert_reqs=ssl.CERT_NONE)
    client.username_pw_set(ACCOUNT, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message_callback
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.loop_start()


def main():
    """
    主函数
    :return:
    """
    try:
        get_registration_code_topic()
        mqtt_connect_main()
        # 延迟2秒，保证连接上
        time.sleep(2)
        send_message(json.dumps(data))
    except Exception as e:
        logger.exception(f"client connect failed, error {e}")


if __name__ == '__main__':
    main()
