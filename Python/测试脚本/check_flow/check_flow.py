import psutil


def network_data():
    """
    获取网卡流量信息
    :return:
    """
    recv = {}
    sent = {}
    data = psutil.net_io_counters(pernic=True)
    interfaces = data.keys()
    for interface in interfaces:
        recv.setdefault(interface, data.get(interface).bytes_recv)
        sent.setdefault(interface, data.get(interface).bytes_sent)
    return interfaces, recv, sent


interfaces, recv, sent = network_data()

print(interfaces)
print(recv)
print(sent)
