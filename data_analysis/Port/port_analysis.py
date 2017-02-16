# encoding:utf-8

"""
分析解析的IP关闭和打开情况
1. 长期探测，发现其打开和关闭的时间分布
2. 关闭的whois的ip的分布
3. 打开的whois的ip的分布

"""

from pymongo import MongoClient
from collections import Counter


def get_db():
    """
    连接数据库
    :return
    """
    client = MongoClient('localhost', 27017)
    db = client['whois_sever_analysis']
    return db


def get_port_state():
    """
    获得有效IP的43端口的状态分布
    :return:
    """
    db = get_db()
    col = db['ip_scan_result']
    ips = col.aggregate([{'$match':{'state':'up'}},{'$group' : {'_id' : "$port_state", 'num' : {'$sum' : 1}}}])
    for i in ips:
        print i


if __name__ == '__main__':

    get_port_state()
