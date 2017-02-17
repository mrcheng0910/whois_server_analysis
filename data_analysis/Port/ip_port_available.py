# encoding:utf-8

"""
分析端口情况，包括是否开放以及开放的服务。
"""

from pymongo import MongoClient
from collections import Counter
from collections import defaultdict


def get_db():
    """
    连接数据库
    :return
    """
    client = MongoClient('localhost', 27017)
    db = client['whois_sever_analysis']
    return db


def get_ip_state():
    """
    获得有效IP的43端口的状态分布
    :return:
    """
    db = get_db()
    col = db['ip_scan_result1']
    ip_status = col.find({},{'_id':0, 'ip':1, 'state':1})


    # dl = defaultdict(list)
    # for i in ip_status:
    #     dl[i['ip']].append(i['state'])

    ds = defaultdict(set)
    for i in ip_status:

        ds[i['ip']].add(i['state'])
    for i in ds:
        if len(ds[i]) > 1:
            print i,ds[i]

    # print dl
    # print ds

if __name__ == '__main__':

    get_ip_state()
