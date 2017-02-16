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


def get_open_down_count():
    """
    获取开放和关闭的ip的数量
    :return:
    """
    db = get_db()
    col = db['ip_scan_result']
    # svr_ip_cur = col.find({'port_service':{'$ne':'whois'}, 'port_state':'open'})
    # svr_ip_cur = col.find({'port_service': 'whois', 'port_state': 'open'},{})
    ip_up = col.find({'state':'up'})
    print 'ips up',ip_up.count()
    ip_down = col.find({'state':'down'})
    print 'ips down',ip_down.count()
    return ip_up,ip_down


def find_svr(ips):
    svrs = []
    db = get_db()
    col = db['com_svr']
    for i in ips:
        svr = col.find({'ips':i['ip']},{'_id':0,'domain':1})
        for s in svr:
            svrs.append(s['domain'])

    print len(svrs)   # 重复的
    print len(list(set(svrs)))   # 去重的
    return svrs



if __name__ == '__main__':

    ip_up, ip_down = get_open_down_count()
    svr_up = find_svr(ip_up)
    svr_down = find_svr(ip_down)
    print list(set(svr_up).intersection(set(svr_down)))   # 端口有开放有关闭的服务器
