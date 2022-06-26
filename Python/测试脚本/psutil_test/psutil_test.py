import psutil
import os
import json
import logging
import configparser

# 读取配置
cf = configparser.RawConfigParser()
cf.read(filenames=r'/usr/lib/kbids/program/kibo_config.ini')

# 上报mac值改为管理口mac值
mac_addr, net_if_addrs = "", psutil.net_if_addrs()
network_interface_path = cf.get("Device-Info", "network_interface_path")


def get_info_from_json(path):
    """
    从json文件中，读取信息
    :param path: json文件路径
    :return: ret
    """
    ret = ""
    try:
        if os.path.exists(path):
            _content = ''
            with open(path, 'r', encoding='utf8') as f:
                for line in f:
                    _content += line
            ret = json.loads(_content)
        else:
            logging.info(f"No such file: {path}")
    except Exception as e:
        logging.exception(f"get info from {path} file failed, error {e}")

    return ret


for net_if_addr in net_if_addrs:
    # 网口开启时
    if net_if_addrs.get(net_if_addr)[0][1] == "10.1.6.100":
        mac_addr = net_if_addrs.get(net_if_addr)[-1][-4].upper()
        logging.info(f"Get mgmt interface mac: '{mac_addr}'")

manage_interface = get_info_from_json(network_interface_path).get("res")

network_mac = psutil.net_if_addrs()[manage_interface][-1][-4].replace("address='", "").replace("'", "")
network_ip = psutil.net_if_addrs()[manage_interface][0][1]

print(network_mac, network_ip)
