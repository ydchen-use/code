"""
远程测试文档
参数说明：
-d： 输入注册码
-c: 输入Linux系统命令，如"ls -l"
-l： 输入要获取的log文件完整，"/usr/lib/kbids/log/xxx.log"
-i: 输入mqtt接口的名称，如“reqBaseInfo”
"""

import paho.mqtt.client as mqtt_client
import json
import time
import ssl
import hashlib
import uuid
import argparse

import threading

SECRET = 'KIBOIDS@3vFUvY8kV89}p;msSWORDFISH$_~{}CMD'

# broker = "in.aiot.swiftsec.com.cn"
broker = "192.168.20.50"
port = 8883

nonce = str(uuid.uuid4())


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--device_id', dest='device_id', help='必填项--输入注册码：')

    parser.add_argument('-c', '--cmd_command', dest='cmd_command', help='选填项--输入的cmd命令： ')

    parser.add_argument('-l', '--log_path', dest='log_path', help='选填项--输入的log完整路径： ')

    parser.add_argument('-i', '--interface', dest='interface', help='选填项--输入mqtt接口名称：reqCheckNetworkRate, '
                                                                    'reqRequireServiceStatus, reqBaseInfo, reqTelnet,'
                                                                    'reqRequireNetcardStatus ')

    _args = parser.parse_args()

    return _args


def connect_mqtt_pub():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Please wait ......")
        else:
            print("Failed %d!", rc)

    client = mqtt_client.Client('934db8f509c343079a0d997ee329b357')
    client.tls_set(ca_certs="my_root_ca.pem", certfile="client.pem", keyfile="client.key", cert_reqs=ssl.CERT_NONE)
    # client.tls_set(ca_certs="/usr/lib/kbids/common/cert/my_root_ca.pem", certfile="/usr/lib/kbids/common/cert/client.pem",
    #                keyfile="/usr/lib/kbids/common/cert/client.key", cert_reqs=ssl.CERT_NONE)
    client.username_pw_set("kibo-swift-term", "kiboterm@2020")
    client.on_connect = on_connect
    client.connect(broker, port, 60)
    return client


def connect_mqtt_sub() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Please wait ......")
        else:
            print("Failed %d!", rc)

    client = mqtt_client.Client('934db8f509c343079a0d997ee329b358')
    client.tls_set(ca_certs="my_root_ca.pem", certfile="client.pem", keyfile="client.key", cert_reqs=ssl.CERT_NONE)
    # client.tls_set(ca_certs="/usr/lib/kbids/common/cert/my_root_ca.pem", certfile="/usr/lib/kbids/common/cert/client.pem",
    #                keyfile="/usr/lib/kbids/common/cert/client.key", cert_reqs=ssl.CERT_NONE)
    client.username_pw_set("kibo-swift-term", "kiboterm@2020")
    client.on_connect = on_connect
    client.connect(broker, port, 60)
    return client


def publish(client):
    msg_count = 0
    param = json.dumps(data)
    while msg_count < 1:
        time.sleep(1)
        # msg = f"message:{msg_count}"
        result = client.publish(topic_pub, param)
        status = result[0]
        if status == 0:
            print("Send message succeed!")
        else:
            print("Failed to send message!")

        msg_count += 1


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        cloud_msg = json.loads(msg.payload.decode("utf-8"))
        methodNameLists = ["reqRequireLog", "reqRequireServiceStatus", "reqBaseInfo", "reqTelnet",
                           "reqRequireNetcardStatus", "reqCheckNetworkRate"]
        try:
            if cloud_msg["methodName"] in methodNameLists:
                cloud_msg = cloud_msg["data"]
                print(f"{cloud_msg}")
            elif cloud_msg["methodName"] == "reqRawCmd":
                cloud_msg = cloud_msg["data"]
                print("args:" + f"{cloud_msg['args']}" + "\n")
                print("code:" + f"{cloud_msg['code']}" + "\n")
                print("stdout:" + f"{cloud_msg['stdout']}" + "\n")
                print("stderr:" + f"{cloud_msg['stderr']}" + "\n")
        except Exception as e:
            print("Revived wrong message!")

    client.subscribe(topic_sub)
    client.on_message = on_message


def run_sub():
    client_sub = connect_mqtt_sub()
    subscribe(client_sub)
    client_sub.loop_forever()


def run_pub():
    client_pub = connect_mqtt_pub()
    client_pub.loop_start()
    publish(client_pub)


def get_data():
    args = parse_args()
    if args.device_id is not None:
        topic_pub = "$kibo/ids/p2p/{device_id}/cloud/req".format(device_id=args.device_id)
        topic_sub = "$kibo/ids/p2p/{device_id}/device/rsp".format(device_id=args.device_id)
        if args.cmd_command is not None:
            encrypt_cmd = hashlib.sha256('{nonce}_{cmd}_{secret}'.format(cmd=args.cmd_command,
                                                                         nonce=nonce,
                                                                         secret=SECRET).encode('utf8')).hexdigest().lower()
            data = {
                "methodName": "reqRawCmd",
                "requestId": nonce,
                "payload": {"auth": encrypt_cmd, "cmd": args.cmd_command, "nonce": nonce}
            }
        elif args.log_path is not None:
            data = {
                "methodName": "reqRequireLog",
                "requestId": "30c9e772-22b8-4446-8084-2e5bde7067f2",
                "payload": {"log_path": f"{args.log_path}"}
            }
        elif args.interface is not None:
            methodnames = {
            "reqRequireServiceStatus":{
                    "methodName": "reqRequireServiceStatus",
                    "requestId": "7929b5e2-f59e-4bdd-b1d2-ba8d01ccd2c4",
                    "payload": {}},
            "reqBaseInfo":{
                    "methodName": "reqBaseInfo",
                    "requestId": "3b369b6b-86f2-4086-8622-834ae7e8ac09",
                    "payload": {}},
            "reqTelnet": {
                    "methodName": "reqTelnet",
                    "requestId": "bfa6557fe3674256b2d2efc411a6cad1",
                    "payload": {
                                "server_port": "17000",
                                "remote_port": "6000"
                                }},
            "reqRequireNetcardStatus":{
                    "methodName": "reqRequireNetcardStatus",
                    "requestId": "aa703d50-7ed7-48db-9d01-1662e6c6018b",
                    "payload": {}},
            "reqCheckNetworkRate":{
                    "methodName": "reqCheckNetworkRate",
                    "requestId": "456841529841",
                    "payload": {
                        "interface": 4
                    }}
            }
            data = methodnames[args.interface]
        else:
            data = {}

    return data, topic_pub, topic_sub


if __name__ == "__main__":
    data, topic_pub, topic_sub = get_data()

    t1 = threading.Thread(target = run_sub, )
    t2 = threading.Thread(target = run_pub, )
    t1.start()
    time.sleep(5)
    t2.start()