# encoding:utf-8

"""
统计分析IP的状态(up/down)，该数据来源于长期针对IP的扫描
1. 发现是否有部分WHOIS服务器定期关机，无法提供查询服务；
2. 发现部分服务器提供查询性能不稳定

@注意：
1. 本地网络对探测的影响
2. 数据库中的时间为UTC+8，分析使用时间为UTC时间

@创建时间：2017年2月15日


"""

from pymongo import MongoClient
from collections import Counter
from collections import defaultdict
import copy
import datetime


def get_db():
    """
    连接数据库
    :return
    """
    client = MongoClient('localhost', 27017)
    db = client['whois_sever_analysis']
    return db

def get_col(col_name = 'ip_scan_result1'):
    """
    获取collection
    :return: col
    """
    db = get_db()
    col = db[col_name]
    return col


def local2utc(d, hours=-8):
    """
    将本地（中国）时间转换为UTC
    :param hours: 转换的时间
    :param d: 时间
    :return: 转换后的时间
    """
    local_time = datetime.datetime.strptime(d,"%Y-%m-%d %H:%M:%S")
    utc_time = local_time + datetime.timedelta(hours=hours)   # utc时间
    return utc_time


def get_ip_state():
    """
    所有IP的长期探测情况
    """
    col = get_col()
    ip_status = col.find({},{'_id': 0, 'ip': 1, 'state': 1, 'detected_time': 1})

    return ip_status


def get_diff_state_ip():
    """
    获取状态不一致的ip列表,开放ip列表，关闭ip列表
    :return:
        diff_ips：状态不一致ips
        up_ips：开放ips
        down_ips: 关闭ips

    """

    diff_ips = []  # 不同状态ip集
    up_ips = []  # 开放状态ip集
    down_ips = []  # 关闭状态ip集
    ds = defaultdict(set)
    ip_status = get_ip_state()
    ip_status_set = copy.deepcopy(ip_status)
    for i in ip_status_set:
        ds[i['ip']].add(i['state'])

    # print len(ds)
    for i in ds:

        if len(ds[i]) > 1:
            diff_ips.append(i)
        else:
            flag = ds[i].pop()
            if flag == 'down':
                down_ips.append(i)
            elif flag == 'up':
                up_ips.append(i)

    # print 'diff_ips',len(diff_ips)
    # print 'up_ips',len(up_ips)
    # print 'down_ips',len(down_ips)

    return diff_ips, up_ips, down_ips


def state_count(diff_ips):
    """
    ip状态计数
    :param diff_ips:
    :return:
    """

    col = get_col()
    for ip in diff_ips:
        ip_details = col.find({'ip':ip},{'_id':0,'detected_time':1,'state':1})
        print ip
        c = Counter()
        for ip in ip_details:
            c[ip['state']] += 1
            print ip['state'], local2utc(ip['detected_time'])
        print 'up', c['up']
        print 'down', c['down']


def state_domain_count(diff_ips):
    """
    分析ip所对应的WHOIS服务器的情况
    :param diff_ips:
    :return:
    """
    col =get_col('com_svr')
    svr_domain = Counter()   # 服务器计数器
    for ip in diff_ips:
        domain = col.find({'ips':ip},{'_id':0,'domain': 1})
        print ip
        print domain.count()
        for d in domain:
            print d
            svr_domain[d['domain']] += 1

    print svr_domain


if __name__ == '__main__':

    # get_ip_state()
    diff_ips, up_ips, down_ips = get_diff_state_ip()
    # state_count(diff_ips)
    # state_domain_count(diff_ips)