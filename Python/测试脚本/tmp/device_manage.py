# coding=utf-8
# This program is definition of key words for RF
import requests
import json
from loguru import logger
import builtins


# 【网络安全中心】【威胁感知设备管理】【配置管理】【资产探测网断配置】开启主动扫描
def edit_monitor_network_segment1(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip+"/swift_cloud_admin_ids_api/controlcenter/editMonitorNetworkSegment"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceId":"KIBOKKMNBZYZ","intervalTime":1,"intervalType":2,"segments":"192.168.0.0/16,172.18.0.0/16","startTime":"01:00","endTime":"23:45","flag":1}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers,data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    assert int(s) == 0


# 【网络安全中心】【威胁感知设备管理】【配置管理】【资产探测网断配置】关闭主动扫描
def edit_monitor_network_segment2(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "/swift_cloud_admin_ids_api/controlcenter/editMonitorNetworkSegment"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceId": "KIBOKKMNBZYZ", "intervalTime": 1, "intervalType": 2,
            "segments": "192.168.0.0/16,172.18.0.0/16", "startTime": "01:00", "endTime": "23:45", "flag": 0}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    assert int(s) == 0


# 【网络安全中心】【威胁感知设备管理】【配置管理】【资产探测网断配置】开启主动扫描, 注册码填写错误
def edit_monitor_network_segment3(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "/swift_cloud_admin_ids_api/controlcenter/editMonitorNetworkSegment"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceId": "KIBOKKMNBZYZwwwww", "intervalTime": 1, "intervalType": 2,
            "segments": "192.168.0.0/16,172.18.0.0/16", "startTime": "01:00", "endTime": "23:45", "flag": 1}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    logger.info(s)

    assert int(s) == -1


# 【网络安全中心】【威胁感知设备管理】【配置管理】【资产探测网断配置】开启主动扫描, 网段填写错误
def edit_monitor_network_segment4(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "/swift_cloud_admin_ids_api/controlcenter/editMonitorNetworkSegment"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceId": "KIBOKKMNBZYZ", "intervalTime": 1, "intervalType": 2,
            "segments": "192.168.0.0/16,172.18.0.0/16,172.18.0.0/10", "startTime": "01:00", "endTime": "23:45", "flag": 1}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    logger.info(s)

    assert int(s) == -1


# 【网络安全中心】【威胁感知设备管理】【配置管理】【资产探测网断配置】开启主动扫描, 时间段填写错误
def edit_monitor_network_segment5(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "/swift_cloud_admin_ids_api/controlcenter/editMonitorNetworkSegment"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceId": "KIBOKKMNBZYZ", "intervalTime": 1, "intervalType": 2,
            "segments": "192.168.0.0/16,172.18.0.0/16", "startTime": "01:10:00", "endTime": "23:45:00", "flag": 1}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    logger.info(s)

    assert int(s) == -1


# 【网络安全中心】【威胁感知设备管理】【配置管理】【资产探测网断配置】开启主动扫描, 网段填写错误，超长字符串
def edit_monitor_network_segment6(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "/swift_cloud_admin_ids_api/controlcenter/editMonitorNetworkSegment"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceId": "KIBOKKMNBZYZ", "intervalTime": 1, "intervalType": 2,
            "segments": "192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16192.168.0.0/16,172.18.0.0/16", "startTime": "01:10", "endTime": "23:45", "flag": 1}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    logger.info(s)

    assert int(s) == -1


# 【网络安全中心】【威胁感知设备管理】【配置管理】【资产探测网断配置】开启主动扫描, 时间段填写错误
def edit_monitor_network_segment7(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "/swift_cloud_admin_ids_api/controlcenter/editMonitorNetworkSegment"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceId": "KIBOKKMNBZYZ", "intervalTime": 1, "intervalType": 2,
            "segments": "192.168.0.0/16,172.18.0.0/16", "startTime": "01:10:00", "endTime": "23:45:00", "flag": 1}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    logger.info(s)

    assert int(s) == -1


# 【网络安全中心】【威胁感知设备管理】【配置管理】【资产探测网断配置】关闭主动扫描, 探测网段填错
def edit_monitor_network_segment8(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "/swift_cloud_admin_ids_api/controlcenter/editMonitorNetworkSegment"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceId": "KIBOKKMNBZYZ", "intervalTime": 1, "intervalType": 2,
            "segments": "192.168.0.0/16,172.18.0.0/16, 172.18.0.0/10", "startTime": "01:00", "endTime": "23:45", "flag": 0}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    assert int(s) == -1


# 【网络安全中心】【威胁感知设备管理】【配置管理】【资产探测网断配置】关闭主动扫描, 时间段填错
def edit_monitor_network_segment9(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "/swift_cloud_admin_ids_api/controlcenter/editMonitorNetworkSegment"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceId": "KIBOKKMNBZYZ", "intervalTime": 1, "intervalType": 2,
            "segments": "192.168.0.0/16,172.18.0.0/16, 172.18.0.0/10", "startTime": "01:00:00", "endTime": "23:45:00", "flag": 0}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    assert int(s) == -1


# 【网络安全中心】【威胁感知设备管理】【配置管理】【snmp配置】添加snmp配置
def edit_monitor_network_segment10(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "swift_cloud_admin_ids_api/controlcenter/addGateWaySwitch"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceFirstIp":"172.18.40.254","deviceLastIp":None,"version":2,"port":161,"timeOut":1,"retry":0,"community":"yuyan@2021","deviceId":"KIBOKKMNBZYZ","switchType":0}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    assert int(s) == 0


# 【网络安全中心】【威胁感知设备管理】【配置管理】【snmp配置】添加snmp配置， ip写错
def edit_monitor_network_segment11(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "swift_cloud_admin_ids_api/controlcenter/addGateWaySwitch"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceFirstIp":"172.18.40.254阿斯顿哈哈是","deviceLastIp":None,"version":2,"port":161,"timeOut":1,"retry":0,"community":"yuyan@2021","deviceId":"KIBOKKMNBZYZ","switchType":0}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    assert int(s) == -1


# 【网络安全中心】【威胁感知设备管理】【配置管理】【snmp配置】添加snmp配置， version填写1，2，3，之外的数字
def edit_monitor_network_segment12(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "swift_cloud_admin_ids_api/controlcenter/addGateWaySwitch"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceFirstIp":"172.18.40.254","deviceLastIp":None,"version":4,"port":161,"timeOut":1,"retry":0,"community":"yuyan@2021","deviceId":"KIBOKKMNBZYZ","switchType":0}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    assert int(s) == -1


# 【网络安全中心】【威胁感知设备管理】【配置管理】【snmp配置】添加snmp配置， port填写字符串
def edit_monitor_network_segment13(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "swift_cloud_admin_ids_api/controlcenter/addGateWaySwitch"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceFirstIp":"172.18.40.254","deviceLastIp":None,"version":2,"port":"161","timeOut":1,"retry":0,"community":"yuyan@2021","deviceId":"KIBOKKMNBZYZ","switchType":0}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    assert int(s) == -1


# 【网络安全中心】【威胁感知设备管理】【配置管理】【snmp配置】添加snmp配置， 团体字填写超长字符串
def edit_monitor_network_segment14(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "swift_cloud_admin_ids_api/controlcenter/addGateWaySwitch"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceFirstIp":"172.18.40.254","deviceLastIp":None,"version":2,"port":161,"timeOut":1,"retry":0,"community":"yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021yuyan@2021","deviceId":"KIBOKKMNBZYZ","switchType":0}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    assert int(s) == -1


# 【网络安全中心】【威胁感知设备管理】【配置管理】【snmp配置】添加snmp配置， 交换机类型填写0，1之外的类型
def edit_monitor_network_segment15(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "swift_cloud_admin_ids_api/controlcenter/addGateWaySwitch"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceFirstIp":"172.18.40.254","deviceLastIp":None,"version":2,"port":161,"timeOut":1,"retry":0,"community":"yuyan@2021","deviceId":"KIBOKKMNBZYZ","switchType":2}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    assert int(s) == -1


# 【网络安全中心】【威胁感知设备管理】【配置管理】【snmp配置】删除snmp配置
def edit_monitor_network_segment16(token, serverip):
    session = requests.session()
    # 设置请求头
    url = serverip + "swift_cloud_admin_ids_api/controlcenter/deleteGateWaySwitch"
    headers = {
        "Host": "192.168.20.69:10000",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "toPath=/login; fromPath=/; clientUrl=/swift_cloud/client/kibo",
        "Origin": "https://192.168.20.69:10000",
        "Referer": "https://192.168.20.69:10000/swift_cloud/login"
    }
    #
    # 将json格式中单引号转换为双引号
    data = {"deviceId":"KIBOKKMNBZYZ","snmpId":"155071bc-0164-49ee-aab8-6f74f2637e59"}

    # post请求发送
    requests.packages.urllib3.disable_warnings()
    response = session.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    resp = json.loads(response.text)
    s = resp["status"]
    assert int(s) == 0


if __name__ == "__main__":
    print("=========")
    edit_monitor_network_segment4("7cd9f98b-fa9c-4fa1-890b-d4a4607f239f", "https://192.168.20.69:10000")
