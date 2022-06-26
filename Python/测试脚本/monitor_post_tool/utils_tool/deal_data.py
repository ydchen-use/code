import uuid
import hashlib
import logging

from setting.mqtt_config import method_names

# 全局变量
REGISTER_CODE = ""  # 注册码
PROBLEM_TYPE = []  # 问题类型
PLATFORM_TYPE = ""  # 平台类型

# 裸命令
SECRET = 'KIBOIDS@3vFUvY8kV89}p;msSWORDFISH$_~{}CMD'

SHELL_CMD = "python3 /usr/lib/kbids/common/monitor_tool/monitor.py -d {device_id} -p {problem_service_list}"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def generate_msg(register_code, problem_type):
    """
    生成发送的msg
    :return:
    """
    global SHELL_CMD
    ret_send_msg = {}
    nonce = str(uuid.uuid4())
    try:
        # 生成 裸命令 请求命令
        SHELL_CMD = SHELL_CMD.format(device_id=register_code, problem_service_list=",".join(problem_type))
        tmp_send_msg = method_names["reqRawCmd"]
        encrypt_cmd = hashlib.sha256('{nonce}_{cmd}_{secret}'.format(cmd=SHELL_CMD,
                                                                     nonce=nonce,
                                                                     secret=SECRET).encode('utf8')).hexdigest().lower()
        tmp_send_msg["requestId"] = nonce
        tmp_send_msg["payload"]["auth"] = encrypt_cmd
        tmp_send_msg["payload"]["cmd"] = SHELL_CMD
        tmp_send_msg["payload"]["nonce"] = nonce
        ret_send_msg = tmp_send_msg
        logger.info(f"send_msg: {ret_send_msg}")
    except Exception as e:
        logger.info(f"generate shell cmd failed, error: {e}")

    return ret_send_msg


def restore_default_value():
    """
    将变量置为默认值
    :return:
    """
    global SHELL_CMD

    # 置为默认值
    SHELL_CMD = "python3 /usr/lib/kbids/common/monitor_tool/monitor.py -d {device_id} -p {problem_service_list}"


def get_post_data(post_data):
    """
    获取post请求的数据 post_data {
                "device_id": "KIBOJAJJJA",
                "problem_type": [1,3],
                "platform_type": 1,
                "time": 1728392837
            }
    :return:
    """
    ret_data = {
        "device_id": "",
        "problem_type": [],
        "platform_type": int,
    }
    try:

        register_code = post_data.get("device_id")  # 设备注册码
        platform_type = post_data.get("platform_type")  # 平台类型
        problem_type = post_data.get("problem_type")  # 问题列表

        # 日志输出
        logger.info(f"register_code: {register_code}")
        logger.info(f"platform_type: {platform_type}")
        logger.info(f"problem_type: {problem_type}")

        ret_data["device_id"] = register_code
        ret_data["platform_type"] = platform_type

        if isinstance(problem_type, list):
            problem_type = [str(item) for item in problem_type]
        elif isinstance(problem_type, str):
            problem_type = problem_type.split(",")

        ret_data["problem_type"] = problem_type

        logger.info(f"PROBLEM_TYPE: {problem_type}")

    except Exception as e:
        logger.info(f"deal data failed, error: {e}")

    return ret_data
