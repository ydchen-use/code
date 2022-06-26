import subprocess
import re


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
        print(output)
        print(type(output))
        print(type(output.decode("utf-8")))
        print(output.decode("utf-8"))
        print(re.findall("suricata\s-c(.*?)\s", output.decode("utf-8")))
        print(err)
        output = output.decode('utf-8').replace("\n", "")
        print(re.findall("suricata\s-c(.*?)bpf", output))
        print(output)
        if 'active' == str(output).lower():
            return True
        else:
            return False
    except Exception as e:
        print("get info failed!")


if __name__ == "__main__":
    is_service_active("tradition")

