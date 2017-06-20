#encoding:utf-8
import socket
import time
def connect_port(ip):
    """
    使用socket与ip的43端口进行连接
    参数
        ip: string 需要验证的ip
    返回值
        True/False: boolean 是否可连接
    """
    port = 43 # whois服务器端口号
    s = socket.socket()
    s.settimeout(30)
    socket_no = s.connect_ex((ip, port),)
    s.close()
    if socket_no == 0:  # 连接成功
        return True
    else:
        return False

start_time = time.time()
# print connect_port('216.21.238.34')
# print connect_port('199.16.128.196')
print connect_port('163.44.75.32')
end_time = time.time()
print end_time - start_time