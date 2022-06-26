def check_tradition():
    """
    无入侵检测
    :return:
    """
    result_dict = {
        "flow": "",
        "service": {},
        "log": {}
    }

    # 最新一条日志时间
    log_last_time = {}
    # 查看相关服务运行情况 tradition
    result_dict_service = check_service(["tradition"])

    # 获取相关日志，最新的时间， real_time_log.log, fast.log, suricata.log
    real_time_log_path = "/usr/lib/kbids/log/real_time_log.log"
    fast_log_path = "/var/log/suricata/fast.log"
    suricata_log_path = "/var/log/suricata/suricata.log"
    log_last_time["real_time_log"] = require_last_time(real_time_log_path)
    log_last_time["fast_log"] = require_last_time(fast_log_path)
    log_last_time["suricata_log"] = require_last_time(suricata_log_path)

    # 检查数据是否正常
    for key in result_dict_service:
        if result_dict_service[key] == "active":
            continue
        else:
            break
    result_dict["service"] = True

    now_time = int(time.time())
    for key in log_last_time:
        if now_time - int(log_last_time[key]) < 86400:
            continue
        else:
            break
    result_dict["log"] = True


def check_decode_dns():
    """
    检测
    :return:
    """
    result_dict = {
        "service": False,
        "log": False
    }

    log_last_time = {}
    # 查看相关服务运行情况 tradition
    result_dict_service = check_service(["decode_dns"])

    # 获取相关日志，最新的时间， decode_dns.log
    decode_dns_path = "/usr/lib/kbids/log/decode_dns.log"
    log_last_time["decode_dns"] = require_last_time(decode_dns_path)

    # 检查数据是否正常
    for key in result_dict_service:
        if result_dict_service[key] == "active":
            continue
        else:
            break
    result_dict["service"] = True

    now_time = int(time.time())
    for key in log_last_time:
        if now_time - int(log_last_time[key]) < 86400:
            continue
        else:
            break
    result_dict["log"] = True


def check_device_status():
    """
    检查device_status
    :return:
    """
    result_dict = {
        "service": False,
        "log": False
    }

    log_last_time = {}
    # 查看相关服务运行情况 tradition
    result_dict_service = check_service(["device_status"])

    # 获取相关日志，最新的时间， decode_dns.log
    device_status_path = "/usr/lib/kbids/log/device_status.log"
    log_last_time["device_status"] = require_last_time(device_status_path)

    # 检查数据是否正常
    for key in result_dict_service:
        if result_dict_service[key] == "active":
            continue
        else:
            break
    result_dict["service"] = True

    now_time = int(time.time())
    for key in log_last_time:
        if now_time - int(log_last_time[key]) < 86400:
            continue
        else:
            break
    result_dict["log"] = True