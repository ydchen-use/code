import subprocess
import configparser
import logging.handlers
import json
import time

from kafka import KafkaProducer

# logging config
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s  %(filename)s:%(lineno)s : %(levelname)s  %(message)s')

# Define a RotatingFileHandler
rfHandler = logging.handlers.RotatingFileHandler(
    filename='/tmp/check_service.log',
    mode='a',
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
)

formatter = logging.Formatter('%(asctime)s  %(filename)s:%(lineno)s : %(levelname)s  %(message)s')
rfHandler.setFormatter(formatter)
rfHandler.setLevel(logging.INFO)

# Create an instance
logging.getLogger('kafka').setLevel(logging.WARNING)
logging.getLogger().addHandler(rfHandler)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 读取配置
cf_def = cf = configparser.RawConfigParser()
cf_def.read(filenames=r'/usr/lib/kbids/program/config.ini')  # 读取mqtt、kakfa相关配置
cf.read(filenames=r'/usr/lib/kbids/program/kibo_config.ini')  # 读取文件配置
REGISTRATION_CODE_PATH = cf.get("Device-Info", "registration_code_path")

# 全局变量
g_kafka_producer = None
g_registration_code = None
g_service_list = ["asset_task", "decode_dns", "device_status", "interrupt_manage", "kbids_master", "passive_iden",
                "patator", "rules_assets_scan", "snmp_task", "suspicious_file_detector", "tradition",
                "kibo_core", "kibo_manage", "kibo_plat_conn"]


# ============Kafka============
KAFKA_BOOTSTRAP_SERVERS = cf_def.get("Kafka", "servers")
ASSET_SCANNED_KAFKA_TOPIC = cf_def.get("Kafka", "asset_scanned")
SASL_PLAIN_USERNAME = cf_def.get("Kafka", "sasl_plain_username")
SASL_PLAIN_PASSWORD = cf_def.get("Kafka", "sasl_plain_password")
SSL_CAFILE = cf_def.get("Kafka", "ssl_cafile")
SSL_CERTFILE = cf_def.get("Kafka", "ssl_certfile")
SSL_KEYFILE = cf_def.get("Kafka", "ssl_keyfile")
CHECK_SERVICE_TOPIC = "check_service_status"


def read_registration_code():
    """
    读取注册码，放入g_registration_code中
    :return: void
    """
    global g_registration_code

    try:
        _content = ''
        with open(REGISTRATION_CODE_PATH, 'r', encoding='utf8') as infile:
            for line in infile:
                _content += line
        g_registration_code = json.loads(_content)['res']
    except:
        g_registration_code = ""
        logger.exception('get_registration_code failed')


def kafka_str_to_list(the_str):
    servers = str(the_str).replace('[', '').replace(']', '').replace('"', '').replace("'", '').split(',')
    return servers


def send_data_to_kafka(topic, dict_data):
    global g_kafka_producer

    if not g_kafka_producer:
        try:
            g_kafka_producer = KafkaProducer(
                sasl_mechanism="PLAIN",
                security_protocol='SASL_SSL',
                sasl_plain_username=SASL_PLAIN_USERNAME,
                sasl_plain_password=SASL_PLAIN_PASSWORD,
                ssl_check_hostname=False,
                ssl_cafile=SSL_CAFILE,
                ssl_certfile=SSL_CERTFILE,
                ssl_keyfile=SSL_KEYFILE,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                bootstrap_servers=kafka_str_to_list(KAFKA_BOOTSTRAP_SERVERS),
                api_version=(1, 1, 1)
            )
            logger.info('create KafkaProducer:{} success'.format(KAFKA_BOOTSTRAP_SERVERS))
        except:
            logger.exception(
                'create KafkaProducer:{} failed'.format(json.dumps(kafka_str_to_list(KAFKA_BOOTSTRAP_SERVERS))))
            g_kafka_producer = None

    if g_kafka_producer:
        try:
            g_kafka_producer.send(topic=topic, value=json.dumps(dict_data))
            g_kafka_producer.flush()
            logger.info("send {} to kafka success".format(dict_data))
        except Exception as e:
            logger.exception('send_device_status_to_kafka failed')


def is_service_active(name):
    """
    检测服务状态
    :param: name 服务名
    :return: True or False
    """
    try:
        # 检测服务状态
        p = subprocess.Popen(["systemctl", "status", name], stdout=subprocess.PIPE)
        (output, err) = p.communicate()
        if 'active' in str(output).lower():
            return True
        else:
            return False
    except Exception as e:
        logger.warning("get info failed!")
        return False


def check_service_status():
    """
    检查服务的状态
    :param service:
    :return:
    """
    global g_service_list
    result_dict = {}
    try:
        for service in g_service_list:
            if is_service_active(service):
                result_dict[service] = "active"
            else:
                result_dict[service] = "inactive"
    except:
        logger.warning("check service failed!")
    return result_dict


def send_result_to_kafka():
    """
    将检查结果发送至kafka
    :return:
    """
    global g_registration_code
    try:
        send_data = {
            "registration_code": g_registration_code,
            "time": time.time(),
            "result": {}
        }
        check_result_dict = check_service_status()
        send_data["result"] = check_result_dict

        send_data_to_kafka(topic=CHECK_SERVICE_TOPIC, dict_data=send_data)
    except:
        logger.warning("send data to kafka failed!")


if __name__ == "__main__":
    read_registration_code()
    send_result_to_kafka()

