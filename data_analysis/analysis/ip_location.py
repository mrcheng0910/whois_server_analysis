# encoding:utf-8
"""
统计IP的地理位置信息
1. 只有1个IP的WHOIS服务器
2. 有多个IP的WHOIS服务器

@作者：程亚楠
@创建时间：2017.3.1
IP定位数据来源于github（https://github.com/lionsoul2014/ip2region）
"""

from ip_location.ip2Region import Ip2Region
from ip_svr_num import get_svr_ip, ip_count
from collections import Counter

searcher = Ip2Region('./ip_location/ip2region.db')  # IP定位


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
    单一IP的地理位置，只分析单个的ip，不包括多于1个的ip
    :return:
    """
    svr_ips = get_svr_ip()
    ips = ip_count(svr_ips)   #ip集合，所有服务器的IP集合，不仅仅包括单个IP
    c = Counter()
    single_count = 0
    for ip in ips:
        if isinstance(ip, list):
            # pass
            for i in ip:
                country = ip2region(i)
                c[country] += 1
                single_count += 1
        else:
            country = ip2region(ip)
            c[country] += 1
            single_count += 1

    print single_count
    for i in c:
        print i, c[i]


def multi_ips_location():
    """
    多个IP的WHOIS服务器分析
    """
    svr_ips = get_svr_ip()
    ips = ip_count(svr_ips)
    c = Counter()

    for ip in ips:
        if isinstance(ip, list):
            print ip
            for i in ip:
                print ip2region(i)
        else:
            country = ip2region(ip)
            c[country] += 1


if __name__ == '__main__':
    ips_location()   # 单一数据分析
    # multi_ips_location()   # 多个ip分析