import re
import time
import os
import fileinput
import enum

from loguru import logger


# time_str1 = "2022-05-25 18:54:56,146  monitor_post.py:67 : INFO"
# time_str2 = "25/5/2022 -- 10:47:25 - <Info> -"
# time_str3 = "04/29/2022-17:15:01.290362  [**]"
# time_str4 = "2022-05-23T10:18:01.005+0800	INFO"
# time_str_list = [time_str1, time_str2, time_str3, time_str4]
# log_list1 = ["2022-05-19 10:03:17,766  sender.py:62 : ERROR  Uncaught error in kafka producer I/O thread",
#              "Traceback (most recent call last):",
#              'File "kafka/producer/sender.py", line 60, in run',
#              'File "kafka/producer/sender.py", line 160, in run_once',
#              'File "kafka/client_async.py", line 582, in poll',
#              'File "kafka/client_async.py", line 392, in _maybe_connect',
#              'File "kafka/conn.py", line 429, in connect',
#              'File "kafka/conn.py", line 508, in _try_handshake',
#              'File "ssl.py", line 1304, in do_handshake',
#              'File "ssl.py", line 1088, in _check_connected',
#              'OSError: [Errno 107] Transport endpoint is not connected', ]
#
# log_list2 = [
#     '21/5/2022 -- 22:02:25 - <Notice> - all 4 packet processing threads, 4 management threads initialized, engine started.',
#     "21/5/2022 -- 22:02:25 - <Info> - Using BPF 'net 192.168.0.0/16 or net 10.0.0.0/8 or net 172.16.0.0/16 or net 20.0.0.0/8 or net 173.231.0.0/16 and not net 58:48:49:24:bd:66' on iface 'br0'",
#     '21/5/2022 -- 22:02:25 - <Error> - [ERRCODE: SC_ERR_AFP_CREATE(190)] - Failed to compile BPF "net 192.168.0.0/16 or net 10.0.0.0/8 or net 172.16.0.0/16 or net 20.0.0.0/8 or net 173.231.0.0/16 and not net 58:48:49:24:bd:66": ethernet address used in non-ether expression',
#     "21/5/2022 -- 22:02:25 - <Error> - [ERRCODE: SC_ERR_AFP_CREATE(190)] - Couldn't init AF_PACKET socket, fatal error",
#     '21/5/2022 -- 22:02:25 - <Error> - [ERRCODE: SC_ERR_FATAL(171)] - thread W#01-br0 failed',
# ]
#
# pattern = re.compile("^\d{1,4}\S\d{1,2}\S\d{1,4}.*\d{1,2}\:\d{1,2}\:\d{1,2}")
#
# for time_str in time_str_list:
#     if pattern.findall(time_str):
#         result = pattern.findall(time_str)
#         print(result)
#         print("right")
#     else:
#         print("wrong")


# ==================  获取日志  =======================


def judge_log_begin_with_time(log_info):
    """
    获取最新日志的时间
    :param log_info: 单条日志信息
    :return:
    """
    ret = {
        "log_time": "",
        "flag": False
    }
    time_pattern = re.compile("^\d{1,4}\S\d{1,2}\S\d{1,4}.*\d{1,2}\:\d{1,2}\:\d{1,2}")
    try:
        if time_pattern.findall(log_info):
            log_time = time_pattern.findall(log_info)[0]
            ret["log_time"] = log_time
            ret["flag"] = True
        logger.info(f"| {log_info} | begin with time | {ret} |")
    except Exception as e:
        logger.warning(f"judge log begin with time failed, error {e}")
    return ret


def verify_time_format(time_str):
    """
    验证时间格式
    :param time_str:
    :return:
    """
    time_stamp = -1
    # python版本程序日志时间格式匹配  2022-05-25 18:54:56
    time_match_pattern1 = re.compile("\d{4}\S\d{1,2}\S\d{1,2}\s\d{1,2}\:\d{1,2}\:\d{1,2}")
    # go版本程序日志时间格式匹配  2022-05-23T10:18:01
    time_match_pattern2 = re.compile("\d{4}\S\d{1,2}\S\d{1,2}\S\d{1,2}\:\d{1,2}\:\d{1,2}")
    # suricata运行日志时间格式匹配  25/5/2022 -- 10:47:25
    time_match_pattern3 = re.compile("\d{1,2}\S\d{1,2}\S\d{4}\s\S{2}\s\d{1,2}\:\d{1,2}\:\d{1,2}")
    # fast.log日志时间格式匹配  04/29/2022-17:15:01
    time_match_pattern4 = re.compile("\d{1,2}\S\d{1,2}\S\d{4}\S\d{1,2}\:\d{1,2}\:\d{1,2}")
    try:
        if time_match_pattern1.findall(time_str):
            time_stamp = time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
        elif time_match_pattern2.findall(time_str):
            time_stamp = time.mktime(time.strptime(time_str, "%Y-%m-%dT%H:%M:%S"))
        elif time_match_pattern3.findall(time_str):
            time_stamp = time.mktime(time.strptime(time_str, "%d/%m/%Y -- %H:%M:%S"))  # 时间戳
        elif time_match_pattern4.findall(time_str):
            time_stamp = time.mktime(time.strptime(time_str, "%m/%d/%Y-%H:%M:%S"))
        else:
            logger.info(f"unknown time format {time_str}")
    except Exception as e:
        logger.warning(f"verify time format failed, error {e}")
    return time_stamp


def require_last_time(log_info, log_path):
    """
    获取日志信息: 最新一条的时间，
    :param: log_info: 日志内容, list or str
    :param: log_path: 日志路径, str
    :return:
    """
    result_dict = {
        "last_time": -1
    }
    try:
        # 获取最新一条带有日期日志的时间
        log_time = ""
        if isinstance(log_info, str):
            judge_result = judge_log_begin_with_time(log_info)
            if judge_result["flag"]:
                log_time = judge_result.get("log_time")
            else:
                logger.info(f"not get time, {log_info}")
                return result_dict
        elif isinstance(log_info, list):
            for log in log_info:
                judge_result = judge_log_begin_with_time(log)
                if judge_result.get("flag"):
                    log_time = judge_result.get("log_time")
                    break

        last_time = verify_time_format(log_time)
        result_dict["last_time"] = last_time
        # logger.info(f"log {log_path.split('/')[-1]} last time : {last_time}")
    except Exception as e:
        logger.info(f"Get log failed! error: {e}")

    return result_dict


def require_log_error(log_info, log_path):
    """
    获取日志中最新的error
    :param: log_info:日志内容, list
    :param: log_path:日志路径, str
    :return: 返回输出结果, str
    """
    result_dict = {
        "error_log": "",
        "error_log_time": -1
    }
    try:
        for log in log_info:
            if " : ERROR" in log or " <Error> " in log:
                # 有报错
                exception_msg = log.strip()
                result_dict["error_log"] = exception_msg

                # 获取该报错时间
                if exception_msg:
                    logger.info(f"error log {exception_msg}")
                    log_time_dict = require_last_time(exception_msg, log_path)
                    result_dict["error_log_time"] = log_time_dict.get("last_time")

                break

    except Exception as e:
        logger.info(f"Get log {log_path}, {log_info} failed! error: {e}")

    return result_dict


def require_log_info(log_path_list):
    """
    获取日志信息
    :param log_path_list:
    :return: 返回输出结果 result_dict = {
        "real_time_log": {
            "log_time": 1786666666.0
            "log": "",
            "log_error": ""
        }
    }
    """
    result_dict = {}
    logger.info(f"log list {log_path_list}")
    try:
        for log_path in log_path_list:
            if os.path.exists(log_path):
                # 日志时间信息
                log_time_dict = {}
                # 日志报错信息
                log_error_dict = {}

                # 获取日志文件最近100行
                log_recent = [line for line in
                              fileinput.input(files=log_path, openhook=fileinput.hook_encoded('utf-8'))][::-1][:99]
                logger.info(f"last 2 log: {log_recent[0:2]}")
                if log_recent:
                    # 获取日志最新的时间
                    log_time_dict = require_last_time(log_info=log_recent, log_path=log_path)
                    logger.info(f"log_time_dict: {log_time_dict}")

                    # 获取报错日志信息
                    log_error_dict = require_log_error(log_recent, log_path)
                    logger.info(f"log_error_dict: {log_error_dict}")

                # 获取日志名称
                log_name = log_path.split("/")[-1].split(".")[0]
                logger.info(f"log_name: {log_name}")
                if log_name:
                    result_dict[log_name] = {}
                    result_dict[log_name]["last_log_time"] = log_time_dict.get("last_time")  # 最新一条日志时间
                    result_dict[log_name]["last_log"] = log_recent[0]  # 最新一条日志
                    result_dict[log_name]["error_log"] = log_error_dict.get("error_log")  # 最新的报错日志
                    result_dict[log_name]["error_log_time"] = log_error_dict.get("error_log_time")  # 最新日志报错时间
            else:
                logger.info(f"log file don't exists, {log_path}")
    except Exception as e:
        logger.exception(f"get log failed, error {e}")

    logger.info(f"require log info : {result_dict}")

    return result_dict


if __name__ == "__main__":
    require_log_info([r"D:\Users\User\Desktop\work-files\code\测试脚本\tmp\snmp_task.log",
                      r"D:\Users\User\Desktop\work-files\code\测试脚本\tmp\suricata.log"])
