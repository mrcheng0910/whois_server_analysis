#encoding:utf-8

import socket
import time
from db_manage import get_db
import random
from  datetime import datetime

import schedule


def get_ips():
    ips = []
    db = get_db()
    col = db['com_svr']
    svr_cur = col.find({}, {'_id': 0, 'ips': 1})
    for svr in svr_cur:
        ips.extend(svr['ips'])

    return list(set(ips))  # 返回去重数据


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
    db = get_db()
    col = db['ip_scan_result_socket1']
    col.insert_one(scan_data)


def main():
    ips = get_ips()
    random.shuffle(ips)
    for ip in ips:

        start_time = time.time()
        # print connect_port('216.21.238.34')
        # print connect_port('199.16.128.196')
        print ip,
        state = connect_port(ip)
        print state,
        end_time = time.time()
        during_time = end_time - start_time
        print during_time
        scan_data = {
            'ip': ip,
            'state': state,
            'during_time': during_time,
            'detected_time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        insert_scan_info(scan_data)


if  __name__ == '__main__':
        # main()
        schedule.every(1.5).hours.do(main)  # 1.5小时循环
        # schedule.every(5).minutes.do(main)

        while True:
            schedule.run_pending()
            time.sleep(1)