import json
import time
import uuid
import ssl
import hashlib
import threading

import paho.mqtt.client as mqtt
from loguru import logger

MQTT_CONFIG = {
    "SERVER_URL": "192.168.20.50",
    # HOST = "in.aiot.swiftsec.com.cn"
    "SERVER_PORT": 8883,  # 端口
    "ACCOUNT": "kibo-swift-term",
    "PASSWORD": "kiboterm@2020",
    "MQTT_CA": "mqtt_config/my_root_ca.pem",
    "MQTT_CERT": "mqtt_config/client.pem",
    "MQTT_KEY": "mqtt_config/client.key",
}


class MyMqtt(threading.Thread):
    # 平台响应等待超时时间
    MQTT_RSP_TIMEOUT = 30  # 单位：秒

    def __init__(self):
        threading.Thread.__init__(self)

        # 类成员初始化
        self.run_flag = True
        self.mqtt_is_connected = False

        self.server_url = None
        self.server_port = None
        self.client_id = None
        self.account = None
        self.password = None
        self.mqtt_ca = None
        self.mqtt_cert = None
        self.mqtt_key = None

        self.device_id = ""

        self.mqtt_client = None
        self.cloud_req_topic = ''
        self.device_rsp_topic = ''

        # 响应数据
        self.cloud_rsp_msg = {}
        self.last_cloud_rsp_time = 0

        # mqtt配置
        self.mqtt_config = {}

        # 初始化mqtt client
        self.__init_mqtt_client__()

    def reload_mqtt_client(self):
        # 初始化topic
        self.__init_topic__()

        # 获取mqtt配置参数
        self.server_url = self.mqtt_config.get("SERVER_URL")
        self.server_port = self.mqtt_config.get("SERVER_PORT")
        self.account = self.mqtt_config.get("ACCOUNT")
        self.password = self.mqtt_config.get("PASSWORD")

        self.mqtt_client.username_pw_set(self.account, self.password)

    def run(self) -> None:
        while self.run_flag:
            try:
                # 重新建立连接
                self.reload_mqtt_client()
                logger.info(f'{self.server_url}:{self.server_port} thread[{threading.current_thread()}] running')
                logger.info(f'current threads: {threading.enumerate()}')

                # 判断是否连接
                if not self.mqtt_is_connected:
                    # 连接服务器
                    self.mqtt_client.connect(self.server_url, self.server_port, 60)
                    self.mqtt_client.loop_forever()

            except Exception as e:
                if self.mqtt_client:
                    self.mqtt_client.disconnect()
                logger.exception(f"mqtt connect failed, error {e}")

            # sleep 5 second, then retry connection
            logger.error('mqtt:{}::{} connection broken'.format(self.server_url, self.server_port))
            self.mqtt_is_connected = False
            time.sleep(5)

    def __init_mqtt_client__(self):
        """
        连接mqtt
        :return:
        """
        # 创建client
        self.client_id = self.get_uuid()
        self.mqtt_client = mqtt.Client(self.client_id)

        # tls set
        self.mqtt_ca = self.mqtt_config.get("MQTT_CA")
        self.mqtt_cert = self.mqtt_config.get("MQTT_CERT")
        self.mqtt_key = self.mqtt_config.get("MQTT_KEY")
        self.mqtt_client.tls_set(ca_certs=self.mqtt_ca,
                                 certfile=self.mqtt_cert,
                                 keyfile=self.mqtt_key,
                                 cert_reqs=ssl.CERT_NONE)

        # callback 函数
        self.mqtt_client.on_connect = self.__on_connect__
        self.mqtt_client.on_message = self.__on_message__
        self.mqtt_client.on_disconnect = self.__on_disconnect__

    def __on_connect__(self, client, userdata, flags, rc):
        # flags是一个包含代理回复的标志的字典；
        # rc的值决定了连接成功或者不成功：0,1,2,3,4,5
        # 0    连接成功
        # 1    协议版本错误
        # 2    无效的客户端标识
        # 3    服务器无法使用
        # 4    错误的用户名或密码
        # 5    未经授权
        self.mqtt_is_connected = True

        # 订阅topic
        self.__subscribe_device_topic__()

        logger.info(f"Mqtt connected, code:{rc}, client_id:[{self.client_id}], client:{client}")

    def __on_disconnect__(self, client, userdata, rc):
        self.mqtt_is_connected = False

        logger.warning("mqtt disconnected!")

    def __on_message__(self, client, userdata, msg):
        try:
            # 对方传过来的是bytes,必须先转成string，再用eval转成dict
            raw_message = str(msg.payload.decode('utf-8')).replace("\n", "").replace("\r", "")
            logger.info("receive cloud msg : |{}|".format(raw_message))
            cloud_msg = json.loads(raw_message)
            # if msg.topic == self.cloud_rsp_topic:
                # self.msg_list.pop(cloud_msg['requestId'])
            self.cloud_rsp_msg[cloud_msg['requestId']] = cloud_msg
            # else:
            #     logger.error('unknown topic: {}'.format(msg.topic))
        except Exception as e:
            logger.exception(f"handle mqtt msg failed, error {e}")

    def __init_topic__(self):
        try:
            self.device_rsp_topic = f"$kibo/ids/p2p/+/device/rsp"
            self.cloud_req_topic = f"$kibo/ids/p2p/{self.device_id}/cloud/req"
        except Exception as e:
            logger.exception(f"init_topics failed, {e}")

    def __subscribe_device_topic__(self):
        """
        订阅缺省 topic
        :return:
        """
        ret = -1
        tp_list = []

        self.__init_topic__()
        try:
            tp_list = [(self.device_rsp_topic, 1)]
            ret, mid = self.mqtt_client.subscribe(tp_list)
        except Exception as e:
            logger.exception(f'subscribe_default_topic failed, error {e}')

        logger.info("subscribe topic [{}] result {}".format(tp_list, ret))
        return ret

    def send_message(self, send_msg):
        # 保证连接上
        while True:
            if self.mqtt_is_connected:
                logger.info("mqtt connect success")
                break
            time.sleep(0.5)

        try:

            rc, mid = self.mqtt_client.publish(self.cloud_req_topic, send_msg, 1)
            logger.info("send msg {} success".format(send_msg))
            send_msg = json.loads(send_msg)
            # 轮询检查是否有返回， 30s无返回则超时
            if rc == 0:
                receive_data = {}
                for i in range(self.MQTT_RSP_TIMEOUT):
                    receive_data = self.cloud_rsp_msg.get(send_msg["requestId"])
                    if receive_data:
                        if receive_data["methodName"] == "reqRawCmd":
                            cloud_msg = receive_data["data"]
                            logger.info("args:" + f"{cloud_msg['args']}" + "\n")
                            logger.info("code:" + f"{cloud_msg['code']}" + "\n")
                            logger.info("stdout:" + f"{cloud_msg['stdout']}" + "\n")
                            logger.info("stderr:" + f"{cloud_msg['stderr']}")
                        else:
                            logger.info('cloud rsp: {}'.format(receive_data["data"]))
                        del self.cloud_rsp_msg[send_msg["requestId"]]
                        break
                    time.sleep(1)
                if not receive_data:
                    logger.info("超时未响应")
        except Exception as e:
            logger.exception(f'send message failed, {e}')

    @staticmethod
    def get_uuid():
        return str(uuid.uuid4()).replace("-", "")

    def get_mqtt_config(self, mqtt_config):
        """
        获取MQTT config
        :param mqtt_config:
        :return:
        """
        self.mqtt_config = mqtt_config

    def get_device_id(self, device_id):
        """
        获取device_id
        :param device_id:
        :return:
        """
        self.device_id = device_id


if __name__ == "__main__":
    data = {
        "methodName": "reqRequireNetcardStatus",
        "requestId": "aa703d50-7ed7-48db-9d01-1662e6c6018b",
        "payload": {}
    }
    my_mqtt = MyMqtt()
    my_mqtt.get_mqtt_config(MQTT_CONFIG)
    my_mqtt.start()

    # for _ in range(5):
    my_mqtt.get_device_id("KIBOBUGEAVDD")
    my_mqtt.send_message(json.dumps(data))

