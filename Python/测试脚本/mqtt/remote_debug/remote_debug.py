from __future__ import print_function
from __future__ import unicode_literals
from prompt_toolkit import *
from prompt_toolkit.history import FileHistory  # 保存历史命令
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory  # 从历史记录中自动提示命令
from prompt_toolkit.contrib.completers import *

import json
import time
import uuid
import ssl
import hashlib

import paho.mqtt.client as mqtt
from loguru import logger

HOST = "8.130.101.19"
PORT = 18883  # 端口
ACCOUNT = "kibo-swift-term"
PASSWORD = "kiboterm@2020"

# 以下是证书路径
MQTT_CA = "my_root_ca.pem"
MQTT_CERT = "client.pem"
MQTT_KEY = "client.key"

# 全局变量
cloud_rsp_msg = {}
publish_topic = ""  # 发布的topic
subscribe_topic = ""  # 订阅的topic
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
    "4": "==> 请输入日志所在绝对路径",
    "5": "==> 请输入网口号，如 ge0",
    "6": "==> 请输入服务名，如 kibo_manage",
    "7": "==> 请输入shell命令，如 ls -l /usr/lib/kbids/log/",
    "8": "==> 请求已发送，请等待5秒，输入exit退出；登陆堡垒机，进行进一步操作！"
}

# method name
method_names = {
    "reqBaseInfo": {
        "methodName": "reqBaseInfo",
        "requestId": "3b369b6b-86f2-4086-8622-834ae7e8ac09",
        "payload": {}},
    "reqRequireServiceStatus": {
        "methodName": "reqRequireServiceStatus",
        "requestId": "7929b5e2-f59e-4bdd-b1d2-ba8d01ccd2c4",
        "payload": {}},
    "reqRequireNetcardStatus": {
        "methodName": "reqRequireNetcardStatus",
        "requestId": "aa703d50-7ed7-48db-9d01-1662e6c6018b",
        "payload": {}},
    "reqRequireLog": {
        "methodName": "reqRequireLog",
        "requestId": "30c9e772-22b8-4446-8084-2e5bde7067f2",
        "payload": {"log_path": ""}},
    "reqCheckNetworkRate": {
        "methodName": "reqCheckNetworkRate",
        "requestId": "456841529841",
        "payload": {
            "interface": ""}},
    "reqServiceRestart": {
        "methodName": "reqServiceRestart",
        "requestId": "3b369b6b86f240868622834ae7e8ac09",
        "payload": {
            "service": "modify_ip",
            "serviceList": ["device_status", "decode_dns"]}},
    "reqRawCmd": {
        "methodName": "reqRawCmd",
        "requestId": nonce,
        "payload": {"auth": "{}", "cmd": "{}", "nonce": nonce}},
    "reqTelnet": {
        "methodName": "reqTelnet",
        "requestId": "bfa6557fe3674256b2d2efc411a6cad1",
        "payload": {
            "server_port": "17000",
            "remote_port": "6000"
        }
    }
}

num_to_method_name = {
    "1": "reqBaseInfo",
    "2": "reqRequireServiceStatus",
    "3": "reqRequireNetcardStatus",
    "4": "reqRequireLog",
    "5": "reqCheckNetworkRate",
    "6": "reqServiceRestart",
    "7": "reqRawCmd",
    "8": "reqTelnet",
}


def on_message_callback(client, userdata, message):
    cloud_msg = json.loads(str(message.payload.decode('utf-8')))
    cloud_rsp_msg[cloud_msg["requestId"]] = cloud_msg


def on_connect(client, userdata, flags, rc):
    global subscribe_topic
    client.subscribe(subscribe_topic)


def on_disconnect(client, userdata, rc):
    mqtt_is_connected = False
    # logger.warning("mqtt disconnected!")


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


def export_help_info():
    """

    :return:
    """
    info_list = ["功能选项--请输入对应数字编号",
                 "(1) 设备基本信息",
                 "(2) 获取服务状态",
                 "(3) 获取网口连接",
                 "(4) 查询日志",
                 "(5) 获取网卡流量(暂时不可用)",
                 "(6) 重启服务",
                 "(7) 裸命令",
                 "(8) 远程连接",
                 "(9) 重新连接",
                 "(10) exit 退出"
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
        # 获取日志
        if service_num == "4":
            print(prompt_msg.get(str(service_num)))
            user_input = prompt(u'>> ', history=FileHistory("history.txt"),
                                auto_suggest=AutoSuggestFromHistory(), completer=BaseCompleter)
            user_input = user_input.strip().lower()  # 进行格式化

            tmp_method_name = num_to_method_name.get(service_num)  # 获取请求的服务名
            tmp_send_msg = method_names.get(tmp_method_name)
            tmp_send_msg["payload"]["log_path"] = user_input
            send_msg = tmp_send_msg  #
        # 获取网卡流量
        elif service_num == "5":
            print(prompt_msg.get(str(service_num)))
            user_input = prompt(u'>> ', history=FileHistory("history.txt"),
                                auto_suggest=AutoSuggestFromHistory(), completer=BaseCompleter)
            user_input = user_input.strip().lower().split(",")  # 进行格式化

            tmp_method_name = num_to_method_name.get(service_num)  # 获取请求的服务名
            tmp_send_msg = method_names.get(tmp_method_name)
            tmp_send_msg["payload"]["interface"] = user_input
            send_msg = tmp_send_msg
        # 重启服务
        elif service_num == "6":
            print(prompt_msg.get(str(service_num)))
            user_input = prompt(u'>> ', history=FileHistory("history.txt"),
                                auto_suggest=AutoSuggestFromHistory(), completer=BaseCompleter)
            user_input = user_input.strip().lower().split(",")  # 进行格式化

            tmp_method_name = num_to_method_name.get(service_num)  # 获取请求的服务名
            tmp_send_msg = method_names.get(tmp_method_name)
            tmp_send_msg["payload"]["serviceList"] = user_input
            send_msg = tmp_send_msg
        # 裸命令
        elif service_num == "7":
            print(prompt_msg.get(str(service_num)))
            user_input = prompt(u'>> ', history=FileHistory("history.txt"),
                                auto_suggest=AutoSuggestFromHistory(), completer=BaseCompleter)
            user_input = user_input.strip().lower()  # 进行格式化

            encrypt_cmd = hashlib.sha256('{nonce}_{cmd}_{secret}'.format(cmd=user_input,
                                                                         nonce=nonce,
                                                                         secret=SECRET).encode('utf8')).hexdigest().lower()

            tmp_method_name = num_to_method_name.get(service_num)  # 获取请求的服务名
            tmp_send_msg = method_names.get(tmp_method_name)
            tmp_send_msg["payload"]["auth"] = encrypt_cmd
            tmp_send_msg["payload"]["cmd"] = user_input
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


def get_user_input():
    """
    获取用户输入
    :return:
    """
    global client
    global need_re_connect
    global need_quit
    req_one_time_list = ["1", "2", "3", "8"]

    try:
        # 获取用户输入
        user_input = prompt(u'>> ', history=FileHistory("history.txt"),
                            auto_suggest=AutoSuggestFromHistory(), completer=BaseCompleter)
        user_input = user_input.strip().lower()  # 进行格式化
        # 如果输入 exit， 则退出
        if user_input == "exit":
            # 断开当前MQTT连接
            client.disconnect()
            client.loop_stop()
            # 主程序退出标志符置为 True
            need_quit = True

        # 如果用户输入9，表示要继续连接设备
        elif user_input == "9":
            # 断开当前MQTT连接
            client.disconnect()
            client.loop_stop()

            # 将重新连接标志符置为 True
            need_re_connect = True
        else:
            pass

        if user_input in req_one_time_list:
            # 获取发送信息
            send_msg = method_names.get(num_to_method_name.get(str(user_input)))
            if user_input == "8":
                print(prompt_msg.get(str(user_input)))
                time.sleep(5)
        else:
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

    client = mqtt.Client(client_id)
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
            logger.exception("运行出错")


if __name__ == '__main__':
    main()

