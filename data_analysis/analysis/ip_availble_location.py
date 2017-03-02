# encoding:utf-8

from ip_location.ip2Region import Ip2Region
from ip_svr_num import  ip_count
from collections import Counter
from pymongo import MongoClient

searcher = Ip2Region('./ip_location/ip2region.db')  # IP定位

def get_db():
    """
    连接数据库
    :return
    """
    client = MongoClient('localhost', 27017)
    db = client['whois_sever_analysis']
    return db


def get_svr_ip():
    """
    获取所有WHOIS地址和ip
    :return:
    """
    ips = []
    db = get_db()
    col = db['ip_scan_result']
    svr_ip_cur = col.find({'state':'up'},{'_id':0, 'ip':1})
    for i in svr_ip_cur:
        # print i
        ips.append(i['ip'])

    return ips


def ip2region(ip=None):
    """
    得到IP的地理位置和运营商
    :param ip: 待查询IP
    :return
        city: ip所在城市，若城市为空，则为国家
        network_operator: 运营商，可能为空
    """
    if ip == "" or ip is None:
        return

    data = searcher.btreeSearch(ip)
    region = data['region']
    region = region.split('|')
    country = region[0]

    return country


def ips_location():
    """

    :return:
    """
    ips = get_svr_ip()
    c = Counter()

    for ip in ips:
        country = ip2region(ip)
        c[country] += 1

    for i in c:
        print i, c[i]


if __name__ == '__main__':
    ips_location()
    # test()
