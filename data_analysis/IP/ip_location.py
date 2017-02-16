# encoding:utf-8

from ip_location.ip2Region import Ip2Region
from ip_svr_num import get_svr_ip, ip_number
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

    :return:
    """
    svr_ips = get_svr_ip()
    ips = ip_number(svr_ips)
    c = Counter()

    for ip in ips:
        if isinstance(ip, list):
            pass
        else:
            country = ip2region(ip)
            c[country] += 1

    for i in c:
        print i, c[i]


def test():
    """

    :return:
    """
    svr_ips = get_svr_ip()
    ips = ip_number(svr_ips)
    c = Counter()

    for ip in ips:
        if isinstance(ip, list):
            print ip
            for i in ip:

                print ip2region(i)
        else:
            country = ip2region(ip)
            c[country] += 1

    # for i in c:
    #     print i, c[i]


if __name__ == '__main__':
    # ips_location()
    test()





# print ip2region('8.8.8.8')