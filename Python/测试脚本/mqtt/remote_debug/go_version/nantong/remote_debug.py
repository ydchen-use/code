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
import hashlib
import os
import subprocess

import paho.mqtt.client as mqtt
from loguru import logger

# HOST = "192.168.20.50"
HOST = "in.aiot.swiftsec.com.cn"
# HOST = "platform.istt.org.cn"
PORT = 8883  # 端口
ACCOUNT = "kibo-swift-term"
PASSWORD = "kiboterm@2020"

# 以下是证书路径
MQTT_CA = "my_root_ca.pem"
MQTT_CERT = "client.pem"
MQTT_KEY = "client.key"

# 全局变量
cloud_rsp_msg = {}
publish_topic = ""  # 发布的topic
subscribe_topic = "test"  # 订阅的topic
register_code = ""  # 注册码
BaseCompleter = SystemCompleter()  # 系统指令自动补全
need_re_connect = True
need_quit = False

# 裸命令
nonce = str(uuid.uuid4())
SECRET = 'KIBOIDS@3vFUvY8kV89}p;msSWORDFISH$_~{}CMD'

# MQTT连接
client: mqtt.Client

# 提示信息
prompt_msg = {
    "1": "==> 请输入shell命令，以英文逗号分隔，如 ls -l /usr/lib/kbids/log/,cat /etc/test.py",
    "2": "==> 请输入url地址， 如 https://swiftsec-pub.oss-cn-hangzhou.aliyuncs.com/main_program_2022_1_11_nantong.img",
    "3": "==> 请输入task_id， 如 1645587272105",
    "4": "==> 请输入shell命令，如 ls -l /usr/lib/kbids/log/"
}

# method name
method_names = {
    "shell": {
        "methodName": "shell",
        "requestId": "3b369b6b-86f2-4086-8622-834ae7e8ac09",
        "payload": {
            "sign": "31720710f6db12f4963122ffdef8f210",
            "cmds": [
                "echo hello > /tmp/test_mqtt.txt",
                "cat /proc/version"]}},
    "upgrade": {
        "methodName": "upgrade",
        "requestId": "3b369b6b-86f2-4086-8622-834ae7e8ac09",
        "payload": {
            "sign": "dc0e7b1b6cca0d900d563255e40a3f50",
            "fileUrl": "https://swiftsec-pub.oss-cn-hangzhou.aliyuncs.com/main_program_2022_1_11_nantong.img"}},
    "query": {
            "methodName": "query",
            "requestId": "3b369b6b-86f2-4086-8622-834ae7e8ac09",
            "payload": {
                "sign": "b20a1d2cfffbc3907ed95b74085fe186",
                "taskId": "1645587272105"}},
}

num_to_method_name = {
    "1": "shell",
    "2": "upgrade",
    "3": "query"
}

# shell 命令
cmd1 = "python3 /usr/lib/test.py -d"


def on_message_callback(client, userdata, message):
    cloud_msg = json.loads(str(message.payload.decode('utf-8')))
    # logger.info(cloud_msg)
    # logger.info(cloud_msg["request_id"])
    # logger.info(type(cloud_msg))
    cloud_rsp_msg[cloud_msg["request_id"]] = cloud_msg
    # logger.info(f"cloud_msg: {cloud_rsp_msg}")


def on_connect(client, userdata, flags, rc):
    global subscribe_topic
    logger.info("Connected with result code " + str(rc))
    client.subscribe(subscribe_topic)


def on_disconnect(client, userdata, rc):
    mqtt_is_connected = False
    logger.warning("mqtt disconnected!")


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
                logger.info(receive_data)
                if receive_data:
                    if receive_data["methodName"] == "reqRawCmd":
                        cloud_msg = receive_data["data"]
                        print("args:" + f"{cloud_msg['args']}" + "\n")
                        print("code:" + f"{cloud_msg['code']}" + "\n")
                        print("stdout:" + f"{cloud_msg['stdout']}" + "\n")
                        print("stderr:" + f"{cloud_msg['stderr']}")
                    else:
                        print('cloud rsp: {}'.format(receive_data["message"]))
                    del cloud_rsp_msg[send_msg["requestId"]]
                    break
                time.sleep(1)
            if not receive_data:
                logger.info("超时未响应")
    except:
        pass


def export_help_info():
    """

    :return:
    """
    info_list = ["功能选项--请输入对应数字编号",
                 "(1) shell命令",
                 "(2) 升级",
                 "(3) 查询升级日志",
                 "(4) 重新连接",
                 "(5) exit 退出"
                 ]
    for info in info_list:
        print(info)


def judge_req(service_num):
    """
    获取MQTT请求方法
    :param service_num:
    :return:
    """
    global prompt_msg
    global num_to_method_name
    global method_names

    send_msg = ""
    try:
        # 执行shell命令
        if service_num == "1":
            print(prompt_msg.get(str(service_num)))
            user_input = prompt(u'>> ', history=FileHistory("history.txt"),
                                auto_suggest=AutoSuggestFromHistory(), completer=BaseCompleter)
            user_input = user_input.strip().lower().split(",")  # 进行格式化

            tmp_method_name = num_to_method_name.get(service_num)  # 获取请求的服务名
            tmp_send_msg = method_names.get(tmp_method_name)
            tmp_send_msg["payload"]["cmds"] = user_input
            send_msg = tmp_send_msg  #
        # 升级
        elif service_num == "2":
            print(prompt_msg.get(str(service_num)))
            user_input = prompt(u'>> ', history=FileHistory("history.txt"),
                                auto_suggest=AutoSuggestFromHistory(), completer=BaseCompleter)
            user_input = user_input.strip().lower()  # 进行格式化

            tmp_method_name = num_to_method_name.get(service_num)  # 获取请求的服务名
            tmp_send_msg = method_names.get(tmp_method_name)
            tmp_send_msg["payload"]["fileUrl"] = user_input
            send_msg = tmp_send_msg
        # 获取升级日志
        elif service_num == "3":
            print(prompt_msg.get(str(service_num)))
            user_input = prompt(u'>> ', history=FileHistory("history.txt"),
                                auto_suggest=AutoSuggestFromHistory(), completer=BaseCompleter)
            user_input = user_input.strip().lower()  # 进行格式化

            tmp_method_name = num_to_method_name.get(service_num)  # 获取请求的服务名
            tmp_send_msg = method_names.get(tmp_method_name)
            tmp_send_msg["payload"]["taskId"] = user_input
            send_msg = tmp_send_msg
    except:
        pass

    return send_msg


def get_registration_code_topic():
    """
    获取 注册码
    mqtt topic
    :return:
    """
    global register_code
    global subscribe_topic
    global publish_topic
    global need_quit

    register_code = input("请输入注册码：").strip()  # 注册码
    if register_code == "exit":
        need_quit = True
    else:
        export_help_info()
        subscribe_topic = f"$kibo/ids/p2p/{register_code}/device/rsp"  # 订阅的topic
        publish_topic = f"$kibo/ids/p2p/{register_code}/cloud/req"  # 发布的topic
        logger.info(f"subscribe_topic: {subscribe_topic}")
        logger.info(f"publish_topic: {publish_topic}")


def get_user_input():
    """
    获取用户输入
    :return:
    """
    global client
    global need_re_connect
    global need_quit
    # req_one_time_list = ["1", "2", "3", "8"]

    try:
        # while True:
        # 获取用户输入
        user_input = prompt(u'>> ', history=FileHistory("history.txt"),
                            auto_suggest=AutoSuggestFromHistory(), completer=BaseCompleter)
        user_input = user_input.strip().lower()  # 进行格式化
        print(user_input)
        # 如果输入 exit， 则退出
        if user_input == "exit":
            # 断开当前MQTT连接
            res1 = client.disconnect()
            print("disconnect res : {}".format(res1))
            stop_res = client.loop_stop()
            print("stop_res : {}".format(stop_res))
            # 主程序退出标志符置为 True
            need_quit = True

        # 如果用户输入4，表示要继续连接设备
        elif user_input == "4":
            # 断开当前MQTT连接
            res1 = client.disconnect()
            print("disconnect res : {}".format(res1))
            stop_res = client.loop_stop()
            print("stop_res : {}".format(stop_res))

            # 将重新连接标志符置为 True
            need_re_connect = True
            # break
        else:
            # pass
            print(threading.currentThread())
            print(threading.enumerate())

        # if user_input in req_one_time_list:
        #     # 获取发送信息
        #     send_msg = method_names.get(num_to_method_name.get(str(user_input)))
        # else:
        send_msg = judge_req(user_input)
        # 发送请求
        if send_msg:
            send_msg = json.dumps(send_msg)
            send_message(send_msg=send_msg)
    except:
        logger.exception("get user input failed!")


def mqtt_connect_main():
    """
    MQTT连接主函数
    :return:
    """
    global client

    # 获取client_id
    client_id = get_uuid()

    client = mqtt.Client(client_id)  # "00:E2:69:11:8D:48_KIBO"
    client.connect(HOST, PORT, 60)
    client.tls_set(ca_certs=MQTT_CA, certfile=MQTT_CERT, keyfile=MQTT_KEY, cert_reqs=ssl.CERT_NONE)
    client.username_pw_set(ACCOUNT, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message_callback
    client.on_disconnect = on_disconnect
    client.loop_start()


def main():
    """
    主函数
    :return:
    """
    global need_re_connect
    global need_quit
    while True:
        try:
            if need_re_connect:
                # 获取注册码，topic
                get_registration_code_topic()
                # 不需要退出主程序时，
                if not need_quit:
                    # MQTT连接主程序
                    mqtt_connect_main()

                    # 重新连接标志符置为False
                    need_re_connect = False
                    # 延迟2秒，保证连接上
                    time.sleep(2)

            # 不需要退出主程序时
            if not need_quit:
                # 如果MQTT连接成功，进行请求
                if client.is_connected():
                    get_user_input()
                else:
                    print("连接失败或断开, 重新连接")
                    # 将重新连接标志符置为True
                    if not need_re_connect:
                        need_re_connect = True
            else:
                break
        except:
            logger.exception("client connect failed!")


if __name__ == '__main__':
    main()

