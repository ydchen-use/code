import json
import time
from kafka import KafkaProducer

patator_log_path = "/usr/lib/kbids/log/patator.log"


# ============Kafka============
# KAFKA_BOOTSTRAP_SERVERS = ['k1.swiftsec.com.cn:9092', 'k2.swiftsec.com.cn:9092', 'k3.swiftsec.com.cn:9092']
KAFKA_BOOTSTRAP_SERVERS = ['in.aiot.swiftsec.com.cn:9092']
KAFKA_TOPIC = 'ids_access_point_req'  # ids_asset_device_req
sasl_plain_username = 'producer'
sasl_plain_password = 'prod-sec@Gd~CTrH]-sV[g]h'
ssl_cafile = r'CARoot.pem'
ssl_certfile = r'certificate.pem'
ssl_keyfile = r'key.pem'


def kafka_str_to_list(the_str):
    servers = str(the_str).replace('[', '').replace(']', '').replace('"', '').replace("'", '').split(',')
    return servers


def send_data_to_kafka():

    g_kafka_producer = KafkaProducer(
        sasl_mechanism="PLAIN",
        security_protocol='SASL_SSL',
        sasl_plain_username=sasl_plain_username,
        sasl_plain_password=sasl_plain_password,
        ssl_check_hostname=False,
        ssl_cafile=ssl_cafile,
        ssl_certfile=ssl_certfile,
        ssl_keyfile=ssl_keyfile,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        # bootstrap_servers=['in.aiot.swiftsec.com.cn:9092'],
        bootstrap_servers=['192.168.20.36:9092', '192.168.20.37:9092', '192.168.20.39:9092'],
        api_version=(1, 1, 1)
    )

    # with open(patator_log_path, 'r') as f:
    #     results = f.read()
    result_dict = {
        "device_id": "KIBOKIOBSWCL",
        "request_id": "ahsaJSDHJAHSDJKA",
        "time": int(time.time()),
        "ip": "192.168.0.111",
        "os": "Windows",
        "port": 7933,
        "protocol": "tcp",
        "server_name": "port['serverName']",
        "server_product": "port['serverProduct']",
        "server_version": "port['serverVersion']",
        "finger_print": "_finger_print",
        "main_page": "",
        "mac": "_mac",
        "mac_factory": "TP-Link",
        "switch_ip": "172.18.40.254",
        "switch_port": 90,
        "switch_host_name": "ruijie",
        "switch_host_type": "KIBOIDS-IDS",
        "switch_brand": "ruijie",
    }
    pri_pick_data = {
        'device_id': 'KIBOKKMNBZYZ',
        'ip': '172.18.128.108',
        'type': 'ua',
        'ttl': '',
        'score': 35,
        'switch_ip': '192.168.128.41',
        'switch_port': 2,
        'switch_host_name': 'GY15#-A2-S2910-1',
        'switch_host_type': 'Ruijie 10G Ethernet Switch(S2910-24GT4XS-E) By Ruijie Networks',
        'switch_real_port': 'GigabitEthernet 0/2',
        'switch_ip_join': '192.168.128.199',
        'switch_real_port_join': 'GigabitEthernet 0/2',
        'switch_host_name_join': 'Ruijie High-density IPv6 100G Core Routing Switch(N18010) By Ruijie Networks',
        'switch_host_type_join': 'Ruijie 10G Ethernet Switch(S2910-24GT4XS-E) By Ruijie Networks',
        'session_num': 4,
        'ua_os': 'Windows,Android',
        'browser_version_map': '{}',
        'phone_type': 'HUAWEI',
        'mac': 'b0:5c:da:93:b3:5f',
        'factory': 'HP Inc.',
        'ua': '[{"ip": "10.81.9.100", "ttl": 63, '
              '"ua": "Dalvik/2.1.0 (Linux; U; Android 10; TAS-AN00 Build/HUAWEITAS-AN00)",'
              ' "ua_browser": "", "ua_browser_version": "", "ua_engine": "", "ua_engine_version": ""}, '
              '{"ip": "10.81.9.100", "ttl": 63, '
              '"ua": "LiveHime/3.50.0.2762 os/Windows pc_app/livehime build/2762 osVer/10.0_x86_64", '
              '"ua_browser": "", "ua_browser_version": "", "ua_engine": "", "ua_engine_version": ""}, '
              '{"ip": "10.81.9.100", "ttl": 63, '
              '"ua": "Mozilla/5.0 BiliDroid/6.31.0 (bbcallen@gmail.com) os/android model/TAS-AN00 '
              'mobi_app/android build/6310200 channel/master innerVer/6310210 osVer/10 network/2", '
              '"ua_browser": "", "ua_browser_version": "", "ua_engine": "", "ua_engine_version": ""}]',
        'time': int(time.time()),
    }

    if result_dict:
        for i in range(20):
            g_kafka_producer.send(topic=KAFKA_TOPIC, value=pri_pick_data)
            g_kafka_producer.flush()
            time.sleep(1)


if __name__ == '__main__':
    send_data_to_kafka()
