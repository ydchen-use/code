import json
import threading
import re
import uuid
import ssl
import time
import logging

import paho.mqtt.client as mqtt

from setting.mqtt_config import mqtt_prompt_msg, platform_type_list, platform_to_config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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

        self.mqtt_client = None
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
            logger.info(f"self.device_rsp_topic: {self.device_rsp_topic}")
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

    def send_message(self, send_msg, device_id):
        ret_dict = {}
        # 保证连接上
        while True:
            if self.mqtt_is_connected:
                logger.info("mqtt connect success")
                break
            time.sleep(0.5)

        try:
            # 发布topic
            cloud_req_topic = f"$kibo/ids/p2p/{device_id}/cloud/req"
            logger.info(f"publish topic : {cloud_req_topic}")
            # 发布消息
            rc, mid = self.mqtt_client.publish(cloud_req_topic, send_msg, 1)
            logger.info("send to topic {} msg {} success".format(cloud_req_topic, send_msg))
            send_msg = json.loads(send_msg)
            # 轮询检查是否有返回， 30s无返回则超时
            receive_data = {}
            if rc == 0:
                for i in range(self.MQTT_RSP_TIMEOUT):
                    receive_data = self.cloud_rsp_msg.get(send_msg.get("requestId"))
                    if receive_data:
                        if receive_data["methodName"] == "reqRawCmd":
                            cloud_msg = receive_data.get("data")
                            logger.info(f"cloud rsp: {cloud_msg}")
                            ret_dict = self.deal_rsp_data(cloud_data=cloud_msg)
                            # logger.info("args:" + f"{cloud_msg['args']}" + "\n")
                            # logger.info("code:" + f"{cloud_msg['code']}" + "\n")
                            # logger.info("stdout:" + f"{cloud_msg['stdout']}" + "\n")
                            # logger.info("stderr:" + f"{cloud_msg['stderr']}")
                        else:
                            ret_dict = receive_data.get("data")
                            logger.info('cloud rsp: {}'.format(receive_data.get("data")))

                        del self.cloud_rsp_msg[send_msg["requestId"]]
                        break
                    time.sleep(1)

                if not receive_data:
                    logger.info(mqtt_prompt_msg.get("mqtt_timeout"))
                    ret_dict = mqtt_prompt_msg.get("mqtt_timeout")
            else:
                ret_dict = mqtt_prompt_msg.get("mqtt_disconnected")
                logger.info("mqtt not connected!")

        except Exception as e:
            logger.exception(f'send message failed, {e}')

        return ret_dict

    @staticmethod
    def get_uuid():
        return str(uuid.uuid4()).replace("-", "")

    @staticmethod
    def deal_rsp_data(cloud_data):
        """
        只处理 裸命令 返回结果
        :param: cloud_data
        :return:
        """
        ret_data = []
        try:
            out_data = cloud_data.get("stderr")
            tmp_data = re.findall("final output: (.*?) end", out_data)[0]
            ret_data = eval(tmp_data)
        except Exception as e:
            logger.exception(f"get rsp cloud data failed, error: {e}")

        return ret_data

    def get_mqtt_config(self, mqtt_config):
        """
        获取MQTT config
        :param mqtt_config:
        :return:
        """
        self.mqtt_config = mqtt_config


def create_instance():
    """
    创建MQTT实例
    :return:
    """
    mqtt_instances = {}
    try:
        for platform_type in platform_type_list:
            mqtt_instances[platform_type] = MyMqtt()
            mqtt_config = platform_to_config.get(platform_type)
            mqtt_instances[platform_type].get_mqtt_config(mqtt_config)
            mqtt_instances[platform_type].start()

    except Exception as e:
        logger.exception(f"create mqtt instance failed! error {e}")

    return mqtt_instances

