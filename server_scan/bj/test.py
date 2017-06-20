#encoding:utf-8

import socket
import time
import random
from  datetime import datetime


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


def main():
    ip = '69.171.248.65'
    print connect_port(ip)

if  __name__ == '__main__':
        main()
