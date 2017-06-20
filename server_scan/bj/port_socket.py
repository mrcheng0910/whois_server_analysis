#encoding:utf-8

import socket
import time
import random
from  datetime import datetime

import schedule


def get_ips():
    ips = []
    svr_file = open('svr_ip.txt','r')
    for i in svr_file.readlines():
        # svr_file.write(i+'\n')
        ips.append(i.strip())
    svr_file.close()

    return ips


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


def insert_scan_info(scan_data):
    """
    Insert the scan info of ip into the db
    :param scan_data:
    :return:
    """
    result_file = open('ip_result.txt','a')
    result_file.write(scan_data+'\n')
    result_file.close()


def main():
    ips = get_ips()
    random.shuffle(ips)
    for ip in ips[:10]:

        start_time = time.time()
        # print connect_port('216.21.238.34')
        # print connect_port('199.16.128.196')
        print ip,
        state = connect_port(ip)
        print state,
        end_time = time.time()
        during_time = end_time - start_time
        print during_time
        scan_data = ip+'\t'+str(state)+'\t'+str(during_time)+'\t'+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_scan_info(scan_data)


if  __name__ == '__main__':
        # main()
        schedule.every(2).hours.do(main)  # 1.5小时循环
        # schedule.every(5).minutes.do(main)

        while True:
            schedule.run_pending()
            time.sleep(1)