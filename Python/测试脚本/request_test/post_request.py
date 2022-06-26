import ast

import requests
import json

from loguru import logger

url = "http://127.0.0.1:5000/remote_monitor"

payload = json.dumps({
    "device_id": "KIBOKKMNBZYZ",
    "problem_type": [1, 3],
    "platform_type": 2,
    "time": 1728392837
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


def obtain_domain_from_third_party(domain):
    """
    调用第三方接口获取域名信息
    :param domain:
    :return:
    """
    ret_dict = {
        "rsp_text": {},
        "status": 0,
        "message": ""
    }
    try:
        url = "http://9sjn2k6pdqsmtxzs1m.swiftsec.com.cn/whoisAPI/getWhois?domainName={domain}".format(domain=domain)

        payload = ""
        headers = {
            'apikey': 'D14DC0E0C8C6701B187679EE87AB7907'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        parse_domain_result = response.text
        logger.info(type(parse_domain_result))   # str
        logger.info(parse_domain_result)
        parse_domain_result = ast.literal_eval(parse_domain_result)  # dict
        logger.info(type(parse_domain_result))
        logger.info(parse_domain_result)
        # if parse_domain_result.get("data"):
        #     ret_dict["message"] = "parse url domain success!"
        # else:
        #     ret_dict["message"] = "parse url domain failed!"
    except Exception as e:
        ret_dict["status"] = -1
        ret_dict["message"] = "get domain info from third party failed, error: " + str(e)
        logger.warning(f"get domain from third party failed, error {e}")

    return ret_dict


if __name__ == "__main__":
    obtain_domain_from_third_party("qzsave.com")
