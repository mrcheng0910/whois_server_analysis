# encoding:utf-8

"""
统计分析IP的状态(up/down)，该数据来源于长期针对IP的扫描
1. 发现是否有部分WHOIS服务器定期关机，无法提供查询服务；
2. 发现部分服务器提供查询性能不稳定
3. 统计长期关闭或者开放的IP和服务器

@注意：
1. 本地网络对探测的影响
2. 数据库中的时间为UTC+8，分析使用时间为UTC时间

@更新时间：2017年2月28日
1. 优化代码

@创建时间：2017年2月15日

"""

from collections import Counter
from collections import defaultdict
import copy

# custom function
from db_manage import get_col
from localtime_to_utc import local2utc


def get_ip_state():
    """
    所有IP的长期探测情况
    """
    col = get_col('ip_scan_result1')
    ip_state = col.find({}, {'_id': 0, 'ip': 1, 'state': 1, 'detected_time': 1})
    return ip_state


def classfy_ip_state():
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
    ip_state = get_ip_state()
    ip_status_set = copy.deepcopy(ip_state)

    # 获取所有ip的状态（去重）
    for i in ip_status_set:
        ds[i['ip']].add(i['state'])

    # IP分类
    for i in ds:
        if len(ds[i]) > 1:    # 多个状态的IP
            diff_ips.append(i)
        else:
            flag = ds[i].pop()  # 一个状态的ip
            if flag == 'down':
                down_ips.append(i)  # 关闭状态
            elif flag == 'up':
                up_ips.append(i)   # 开放状态

    return diff_ips, up_ips, down_ips


def pure_domain_state(ips):
    """
    分析全部关闭或者打开的服务器域名
    :param ips: ip列表
    :return:
        domain: list，服务器域名
    """
    col = get_col('com_svr')
    domains = set()
    for ip in ips:
        domain = col.find({'ips': ip}, {'_id': 0, 'domain': 1})
        for d in domain:
            domains.add(d['domain'])

    return list(domains)


def state_count(diff_ips):
    """
    ip状态计数
    :param diff_ips:
    :return:
    """

    col = get_col('ip_scan_result1')
    for ip in diff_ips:
        scan_info = col.find({'ip': ip}, {'_id': 0, 'detected_time': 1, 'state': 1})
        c = Counter()
        for i in scan_info:
            c[i['state']] += 1
            # print ip['state'], local2utc(ip['detected_time'])
        print ip, c['up'], c['down']
        # print 'up', c['up']
        # print 'down', c['down']


def state_domain_count(diff_ips):
    """
    分析ip所对应的WHOIS服务器的情况
    :param diff_ips:
    :return:
    """
    col = get_col('com_svr')
    svr_domain = Counter()  # 服务器计数器
    for ip in diff_ips:
        domain = col.find({'ips': ip}, {'_id': 0, 'domain': 1})
        print ip
        print domain.count()
        for d in domain:
            print d
            svr_domain[d['domain']] += 1

    print svr_domain


if __name__ == '__main__':

    diff_ips, up_ips, down_ips = classfy_ip_state()
    print len(down_ips)
    for ip in down_ips[0:5]:
        print ip

    # 对经过长期探测的状态稳定的服务器（IP和domain）进行统计
    up_domains = pure_domain_state(up_ips)  # 开放的WHOIS服务器
    down_domains = pure_domain_state(down_ips)  # 关闭的服务器

    instability_domain = set(up_domains) & set(down_domains)  # 不稳定服务器
    # print list(instability_domain)
    # print len(instability_domain)

    # 长期打开服务器
    # long_term_up_domains = list(set(up_domains)-instability_domain)
    # print long_term_up_domains
    # print len(long_term_up_domains)

    # 长期关闭服务器
    long_term_down_domains = list(set(down_domains)-instability_domain)
    print  long_term_down_domains
    # print len(long_term_down_domains)
    # state_count(diff_ips)
    # state_domain_count(diff_ips)
