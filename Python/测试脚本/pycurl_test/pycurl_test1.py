"""
可用性测试代码，使用实例测试
"""
import pycurl

from loguru import logger


def request_url(url: str, timeout_time: int) -> dict:
    """
    执行request请求，获取响应码，响应时间
    :param url:
    :param timeout_time
    :return:
    """
    ret_dict = {
        "rsp_code": None,
        "rsp_time": None,
        "rsp_connect_time": None
    }
    try:

        c = pycurl.Curl()  # 创建一个Curl对象

        c.setopt(pycurl.URL, url)  # 定义请求的URL常量
        c.setopt(pycurl.CONNECTTIMEOUT, 5)  # 定义请求连接的等待时间
        c.setopt(pycurl.TIMEOUT, timeout_time)  # 定义请求超时时间
        c.setopt(pycurl.NOPROGRESS, 1)  # 屏蔽下载进度条
        c.setopt(pycurl.FORBID_REUSE, 1)  # 完成交互后强制断开连接,不重用
        c.setopt(pycurl.MAXREDIRS, 1)  # 指定HTTP重定向的最大数为1
        c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)  # 设置保存DNS信息的时间为30秒

        try:
            c.perform()  # 提交请求
            connect_time = c.getinfo(c.CONNECT_TIME)  # 获取建立连接时间
            http_code = c.getinfo(c.HTTP_CODE)  # 获取HTTP状态码
            total_time = c.getinfo(c.TOTAL_TIME)  # 获取传输的总时间

            ret_dict["rsp_code"] = http_code
            ret_dict["rsp_time"] = total_time * 1000
            ret_dict["rsp_connect_time"] = connect_time * 1000
        except Exception as e:
            logger.info("connection error:" + str(e))
            c.close()

    except Exception as e:
        logger.warning(f"request url failed, error: {e}")

    return ret_dict


if __name__ == "__main__":
    URL = "http://qzsave.com"
    timeout_time = 1

    ret_dict1 = request_url(URL, timeout_time)

    print(ret_dict1)
