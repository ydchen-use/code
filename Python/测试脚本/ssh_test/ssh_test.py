import paramiko
from time import *


# 定义一个类， 表示一个ssh连接
class SSHClient(object):
    # 通过ip，port，用户名，密码，超时时间初始化一个远程服务器
    def __init__(self, ip, port, username, password, timeout=30):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
        # transport 和 channel
        self.t = ''
        self.chan = ''
        # 连接失败的重试次数
        self.try_times = 3

    # 使用该方法连接远程主机
    def connect(self):
        while True:
            # 连接过程中可能会抛出异常，比如网络不通、连接超时
            try:
                self.t = paramiko.Transport(sock=(self.ip, self.port))
                self.t.connect(username=self.username, password=self.password)
                self.chan = self.t.open_session()
                self.chan.settimeout(self.timeout)
                self.chan.get_pty()
                self.chan.invoke_shell()
                # 如果没有抛出异常说明连接成功，直接返回
                print("连接%s成功", self.ip)
                # 接收到的数据解码为str
                print(self.chan.recv(65535).decode("utf-8"))
                return
            # 这里不对可能的异常如socket.error, socket.timeout细化，一网打尽
            except Exception as e:
                if self.try_times != 0:
                    print("连接%s失败，进行重试", self.ip)
                    self.try_times -= 1
                else:
                    print("重试3次结束， 结束程序")
                    exit(1)

    # 断开连接
    def close(self):
        self.chan.close()
        self.t.close()

    # 发送要执行的命令
    def send(self, cmd):
        cmd += '\r'
        result = ''
        # 发送执行的命令
        self.chan.send(cmd)
        # 回显很长的命令可能要执行很久，通过循环分批次取回回显，执行成功后返回True， 失败返回False
        while True:
            sleep(0.5)
            ret = self.chan.recv(65535)
            ret = ret.decode("utf-8")
            result += ret
            return result

    """
    发送文件
    @:param upload_files 上传文件路径，例如: /tmp/test.py
    @:param upload_path 上传到目标路径， 例如：/tmp/test_new.py
    """
    def upload_file(self, upload_files, upload_path):
        try:
            tran = paramiko.Transport(sock=(self.ip, self.port))
            tran.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(tran)
            result = sftp.put(upload_files, upload_path)
            return True if result else False
        except Exception as ex:
            print(ex)
            tran.close()
        finally:
            tran.close()


if __name__ == "__main__":
    # ssh = SSHClient("172.18.133.108", 19022, "kbadmin", "t(Tz4gO=agt&y.9k")
    ssh = SSHClient("8.133.169.245", 22, "kbdev", "kbwaf@Kibo#2020")
    ssh.connect()

    def input_cmd(str):
        return input(str)
    tishi_msg = "输入命令："
    while True:
        msg = input(tishi_msg)
        if msg == "exit":
            ssh.close()
            break
        else:
            res = ssh.send(msg)
            data = res.replace(res.split("\n")[-1], "")
            tishi_msg = res.split("\n")[-1]
            print(res.split("\n")[-1] + data.strip("\n"))

