# encoding:utf-8

"""
服务器解析的IP数量的统计
1. 各个服务器解析出IP数量分布
2. 总共解析出的IP集
3. 各个IP表示的服务器数量分布，存在一对多的情况
@作者：程亚楠
@创建时间：2017.3.1

"""

from collections import Counter
from db_manage import get_col


def get_svr_ip():
    """
    获取所有域名和ip
    :return:
    """

    col = get_col('com_svr')
    svr_ips = col.find({},{'_id': 0, 'ips': 1, 'domain': 1})
    return svr_ips


def ip_number_distribution(svr_ips):
    """
    WHOIS服务器解析ip数量分布统计
    :param svr_ips:  记录集合
    """
    c = Counter()
    for i in svr_ips:
        ip_count = len(i['ips'])  # 域名解析IP的数量

        if ip_count != 1:
            print i['domain'], ip_count  # 输出IP数量大于1的服务器

        c[ip_count] += 1  # 求IP数量的分布

    print 'IP number Count',"WHOIS count"
    for i in c:
        print i, c[i]


def ip_count(svr_ips):
    """
    总共ip数量统计
    @todo:应该求iP集，而不是独立IP
    :param svr_ips:
    :return:
    """
    ips = []
    single_ips = []
    for i in svr_ips:
        if len(i['ips']) == 1:
            single_ips.extend(i['ips'])
        else:
            if i['ips']:   # 去掉空集
                ips.append(i['ips'])
    ips.extend(list(set(single_ips)))
    print "IP总数，说明WHOIS服务器共用ip"
    print len(ips)
    return ips


def ip_svr_number(svr_ips):
    """
    ip所负责WHOIS服务器的分布
    :param svr_ips:

    """
    c = Counter()
    for i in svr_ips:
        if len(i['ips']) == 1:
            c[i['ips'][0]] += 1

    for i in c:
        print i,c[i]

if __name__ == '__main__':


    svr_ips = get_svr_ip()
    # svr_ips_dist = svr_ips.clone()
    # ip_number_distribution(svr_ips_dist)   # 服务器解析IP数量分布
    # ip_numbers = svr_ips.clone()
    # ip_count(ip_numbers)
    ip_svr_number(svr_ips)
    print "结束"