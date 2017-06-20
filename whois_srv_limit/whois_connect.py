# encoding:utf-8
"""
    whois服务器通信
=====================
"""

import socks
import time

TIMEOUT = 30  # 超时设定

class GetWhoisInfo:
    """whois 通信类"""

    def __init__(self, domain, whois_srv):
        """处理whois服务器"""
        self.request_data = domain
        self.whois_srv = whois_srv

    def get(self):
        """获取数据"""
        data = self._connect()
        return data

    def _connect(self):
        """核心函数：与whois通信
        需要：socks.py (ver 1.5.7)"""
        # whois服务器ip，代理ip
        global _proxy_socks
        self.tcpCliSock = socks.socksocket()  # 创建socket对象
        self.tcpCliSock.settimeout(TIMEOUT)  # 设置超时时间
        data_result = ""
        try:
            self.tcpCliSock.connect((self.whois_srv, 43))  # 连接whois服务器
            self.tcpCliSock.send(self.request_data + '\r\n')  # 发出请求
        except Exception as e:  # Exception来自socks.py 中设置的异常
            print str(e)
            return str(e)
        # 接收数据
        while True:
            try:
                data_rcv = self.tcpCliSock.recv(1024)  # 反复接收数据
            except Exception, e:
                print str(e)
                self.tcpCliSock.close()
                time.sleep(5)
                return str(e)
            if not len(data_rcv):
                self.tcpCliSock.close()
                return data_result  # 返回查询结果

            data_result = data_result + data_rcv  # 每次返回结果组合
