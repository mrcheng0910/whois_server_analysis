# encoding: utf-8
"""
根据IP获取二级服务器的域名
"""

from data_analysis.analysis_svr.db_manage import get_col
from collections import defaultdict


def get_ip():
    ips = []
    ip_file = open('IP.txt','r')
    for ip in ip_file:
        ips.append(ip.strip())

    return ips


def get_svr():
    d = defaultdict(set)
    ips = get_ip()
    col = get_col('com_svr')
    for ip in ips:
        svr = col.find({'ips':ip},{'_id':0,'domain':1})
        for i in svr:
            d[ip].add(i['domain'])

    for i in d:
        print i, list(d[i])[0]
    print len(d)


get_svr()









