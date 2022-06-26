import json
import logging.handlers
import time

from flask import Flask, request

from utils_tool.deal_data import get_post_data, generate_msg, restore_default_value
from utils_tool.mqtt_connect import create_instance
from setting.mqtt_config import num_to_platform_type

app = Flask(__name__)

g_mqtt_instances = {}

# logging config
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s  %(filename)s:%(lineno)s : %(levelname)s  %(message)s')

# Define a RotatingFileHandler
# /home/kbdev/ids-diag/remote_program/monitor_tool/log_file/monitor_post.log
rfHandler = logging.handlers.RotatingFileHandler(
    filename='../monitor_post_tool/log_file/monitor_post.log',
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


@app.route("/remote_monitor", methods=["POST"])
def remote_monitor():
    # logger.info(f"post request headers: {request.headers}")
    logger.info(type(request.json))
    logger.info(f"post request body: {request.json}")

    # 获取post data
    post_data_dict = get_post_data(request.json)
    logger.info(f"post data : {post_data_dict}")

    # 获取发送的mqtt方法
    send_msg = generate_msg(post_data_dict.get("device_id"), post_data_dict.get("problem_type"))

    # 获取mqtt连接实例
    platform_type = num_to_platform_type.get(str(post_data_dict.get("platform_type")))
    logger.info(f"platform_type : {platform_type}")
    mqtt_client_current = g_mqtt_instances.get(platform_type)

    # 发送mqtt请求
    rsp_result = mqtt_client_current.send_message(send_msg=json.dumps(send_msg), device_id=post_data_dict.get("device_id"))

    # 获取结果
    result = rsp_result

    # 将变量置为默认值
    restore_default_value()

    logger.info(f"return result: {result}")
    return json.dumps(result)


if __name__ == "__main__":
    while True:
        # 创建MQTT实例
        if not g_mqtt_instances:
            g_mqtt_instances = create_instance()
            logger.info(f"Now g_mqtt_instances : {g_mqtt_instances}")

        try:
            host = "127.0.0.1"
            port = 5000
            app.run(host=host, port=port)

            logging.info(f'listening to {host} : {port}')
        except Exception as e:
            logger.exception(f"start flask failed, retry later, error {e}")
            time.sleep(20)
