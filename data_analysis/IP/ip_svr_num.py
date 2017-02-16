# encoding:utf-8

"""
分析服务器的ip在数量上的情况
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


def get_svr_ip():
    """
    获取所有WHOIS地址和ip
    :return:
    """
    svr_ips = []
    db = get_db()
    col = db['com_svr']
    svr_ip_cur = col.find({},{'_id':0, 'ips':1, 'domain':1})
    for i in svr_ip_cur:
        # print i
        svr_ips.append(i)

    return svr_ips


def ip_number_distribution(svr_ips):
    """
    WHOIS服务器的ip数量分布统计
    :param svr_ips:
    :return:
    """
    c = Counter()
    for i in svr_ips:
        # print i
        # print i['ips']
        c[len(i['ips'])] += 1

    for i in c:
        print 'ip number:', i, 'amount:', c[i]

    return c


def ip_number(svr_ips):
    """
    总共ip数量统计
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


def ip_svr_number(svr_ips):
    """
    ip所负责WHOIS服务器的分布
    :param svr_ips:
    :return:
    """
    c = Counter()
    for i in svr_ips:
        for ip in i['ips']:
            c[ip] += 1

    print c
    for i in c:
        print i,c[i]

if __name__ == '__main__':

    # draw()
    svr_ips = get_svr_ip()
    ip_number_distribution(svr_ips)   # 服务器解析IP数量分布
    ip_number(svr_ips)
    ip_svr_number(svr_ips)