# encoding:utf-8

"""
使用nmap的tcp sys或udp探测ip的43端口开放情况，并且存入到数据库中,循环探测
"""

from datetime import datetime
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
from time import sleep
from db_manage import get_db
import random
import schedule
import time


def get_scanning_ip():
    """
    获取被扫描的IP数据集
    :return:  ips
    """
    ips = []
    db = get_db()
    col = db['com_svr']
    svr_cur = col.find({},{'_id':0,'ips':1})
    for svr in svr_cur:
        ips.extend(svr['ips'])

    return list(set(ips))  # 返回去重数据


def insert_scan_info(scan_data):
    """
    Insert the scan info of ip into the db
    :param scan_data:
    :return:
    """
    db = get_db()
    col = db['ip_scan_result1']
    col.insert_one(scan_data)


class ServerInfo(object):

    def __init__(self,ip,options="-sV"):
        """
        初始化函数
        :param ip:
        :param source:
        :param options:
        """
        self.ip = ip  # 探测的ip
        self.options = options  #nmap探测命令

        # 参数
        self.detected_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.elapsed = 0   # 探测时间
        self.status = ""     # ip状态：up/down
        self.host_name = ""  # ip逆向解析
        self.portid = 0
        self.protocol = ""
        self.port_state = ""
        self.service = ""
        self.banner = ""

        # 原始数据
        self.raw_data = ""
        self.parsed = None

    def do_scan(self):
        """
        对targets进行扫描，并返回探测结果
        :param targets: 扫描目标
        :param options: 扫描选项
        :return:
        """
        nmproc = NmapProcess(self.ip, self.options)
        nmproc.run_background()  # 在后台运行
        while nmproc.is_running():
            nmaptask = nmproc.current_task
            if nmaptask:
                print("Task {0} ({1}): ETC: {2} DONE: {3}%".format(nmaptask.name,
                                                                   nmaptask.status,
                                                                   nmaptask.etc,
                                                                   nmaptask.progress))
            sleep(2)
        self.raw_data = nmproc.stdout  # 原始扫描数据
        try:
            self.parsed = NmapParser.parse(nmproc.stdout)  # 解析扫描的数据
        except NmapParserException as e:
            print("Exception raised while parsing scan: {0}".format(e.msg))
            return

    def print_scan(self):
        """
        解析扫描结果
        """
        nmap_report = self.parsed   # 解析数据
        down_ip_file = open('down_ip.txt','a')
        if not nmap_report:   # 如果ip关闭，则结束
            self.status = 'down'
            self.host_name = self.ip
            down_ip_file.write(self.host_name+'\t' + datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')    # 把关闭的ip写入文件
            down_ip_file.close()
            return

        for host in nmap_report.hosts:

            # 得到反解析的域名，若无则未探测ip
            if len(host.hostnames):
                self.host_name = host.hostnames.pop()
            else:
                self.host_name = host.address

            self.status = host.status  # host状态，up开放/down关闭
            self.elapsed = nmap_report.elapsed  # 探测时长

            # 如果host关闭状态，则结束
            if self.status=='down':
                return

            # 否则继续执行

            for serv in host.services:
                self.port_state=serv.state
                self.service=serv.service
                self.banner = serv.banner
                self.portid = serv.port
                self.protocol = serv.protocol

    def print_server(self):

        server_dic = {
            "ip": self.ip,
            "hostname":self.host_name,
            "elapsed": self.elapsed,
            "state": self.status,
            "detected_time": self.detected_time,
            "portid": self.portid,
            "port_state": self.port_state,
            "port_service": self.service,
            "port_banner": self.banner,
            "port_protocol": self.protocol,
            "scan_source":'172.29.152.152'
        }
        print server_dic
        insert_scan_info(server_dic)

    def scan_result(self):

        self.do_scan()    # 扫描端口
        self.print_scan()
        self.print_server()


def main():
    detect_server = get_scanning_ip()
    random.shuffle(detect_server)    # 把ip随机，这样每次探测的时候，时间都不一样
    ip_count = len(detect_server)
    for ip in detect_server:
        print ip
        # t = ServerInfo(str(ip), "-sV -sU -p 43")  # 使用udp协议扫描,需在管理员权限下运行
        t = ServerInfo(str(ip), "-sV -p 43")  # 使用tcp协议扫描
        t.scan_result()
        ip_count -= 1
        print ip_count  # 剩余扫描数量


if __name__ == "__main__":

    schedule.every(7).hours.do(main)   # 7小时循环
    # schedule.every(5).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)