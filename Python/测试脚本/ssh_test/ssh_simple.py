import paramiko


# 建立一个sshclient对象
ssh = paramiko.SSHClient()

# 允许将信任的主机自动加入到host_allow列表，此方法必须放在connect方法的前面
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 调用connect方法连接服务器
ssh.connect(hostname="172.18.133.108", port=19022, username="kbadmin", password="t(Tz4gO=agt&y.9k")

# 执行shell命令
stdin, stdout, stdeer = ssh.exec_command("df -hl")

# 将结果放到stdout中，如果有错误将放到stderr中
print(stdout.read().decode())

# 关闭连接
ssh.close()
