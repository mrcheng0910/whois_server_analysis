# encoding:utf-8

"""
使用nmap的tcp sys探测ip的端口开放情况，并且存入到数据库中
"""

from datetime import datetime
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
from time import sleep


class ServerInfo(object):



    def __init__(self,ip,source,options="-sV",method="tcp_syn"):
        """
        初始化函数
        :param ip:
        :param source:
        :param options:
        """
        self.ip = ip  # 探测的ip
        self.source = source  # ip来源，
        self.options = options  #nmap探测命令
        self.method = method  # 探测方法

        # 参数
        self.detected_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.filter_port_count = 0  # 未知端口数量
        self.closed_port_count = 0  # 关闭端口数量
        self.open_port_count = 0  #开放端口数量
        self.ports = []   # 端口详细信息
        self.elapsed = 0   # 探测时间
        self.status = ""     # ip状态：up/down
        self.host_name = ""  # ip逆向解析

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
        nmap_report = self.parsed


        if not nmap_report:
            self.status = 'down'
            self.host_name = self.ip
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

            port_closed = port_open = port_filter = 0

            for serv in host.services:
                tmp_port = serv.port
                tmp_protocol=serv.protocol
                tmp_state=serv.state
                tmp_service=serv.service
                tmp_banner = serv.banner


                self.ports.append({
                    "portid":tmp_port,
                    "protocol": tmp_protocol,
                    "state":tmp_state,
                    "service":tmp_service,
                    "banner":tmp_banner
                })

                if tmp_state == 'open':
                    port_open += 1
                elif tmp_state == 'closed':
                    port_closed +=1
                elif tmp_state == 'filtered':
                    port_filter += 1

            self.open_port_count = port_open
            self.closed_port_count = port_closed
            self.filter_port_count = port_filter
            if port_filter == 0 and port_closed==0:
                self.filter_port_count = 100 - port_open
            elif port_filter == 0 and port_closed!=0:
                self.filter_port_count = 100 - port_open-port_closed
            elif port_filter != 0 and port_closed==0:
                self.closed_port_count = 100 - port_open-port_filter


    def print_server(self):

        server_dic = {
            "ip": self.ip,
            "hostname":self.host_name,
            "source": self.source,
            "filter_count": self.filter_port_count,
            "closed_count": self.closed_port_count,
            "open_count": self.open_port_count,
            "ports": self.ports,
            "elapsed": self.elapsed,
            "state": self.status,
            "detected_time": self.detected_time,
            "method": self.method
        }
        print server_dic
        print self.raw_data
        # from db_manage import insert_detect_info
        # insert_detect_info(server_dic)

    def scan_result(self):

        self.do_scan()
        self.print_scan()
        self.print_server()

if __name__ == "__main__":

    detect_server = ['116.255.241.227']

    for ip in detect_server:
        t = ServerInfo(ip.strip(), "dns","-sV -p 43","tcp-syn")
        t.scan_result()
