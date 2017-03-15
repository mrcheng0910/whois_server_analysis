# encoding:utf-8

"""
获取WHOIS地址的IP地址，并且更新数据库

作者：程亚楠
时间：2017.2.15
"""

from datetime import datetime
import dns.resolver
from db_manage import get_db
import schedule
import time

def domain2ip(domain):
    """
    获取解析到的域名IP列表
    参数
        domain: string 待解析的域名

    返回值
        ips: list 域名解析后的ip列表
    """

    ips = []
    res = dns.resolver.Resolver()
    # 防止dns服务器拒绝服务，使用多个dns服务器
    res.nameservers = ['8.8.8.8', '8.8.4.4', '114.114.114.114', '208.67.222.222', '223.5.5.5','223.6.6.6']

    try:
        domain_ip = res.query(domain, 'A')
        for i in domain_ip:
            ips.append(i.address)
    except:
        ips = []
    return ips


def insert_db(domain,ips=None):
    """
    把ip更新到数据库中
    :param domain:  待更新域名
    :param ips:  更新的ips
    """
    db = get_db()
    col = db['com_svr']
    col.update(
        {'domain': domain},
        {
            '$set': {'ips':ips}
        },
        False,
        True
    )  # 修改某字段


def get_svr():
    """
    获取域名WHOIS服务器的域名地址和ip列表
    :return:
    svrs: 服务器域名和ip列表
    """
    svrs = []
    db =get_db()
    col = db['com_svr']
    svr_cur = col.find(
        {},
        {   # 指定获取字段
            '_id': 0,
            'domain': 1,
            'ips': 1
        }
    )
    for svr in svr_cur:
        svrs.append(svr)

    return svrs


def get_svr_ip():
    """
    获取服务器的IP地址，并与已有ip比对,最后更新数据库
    """
    import random

    svrs = get_svr()
    random.shuffle(svrs)  # 将列表进行随机
    svr_count = len(svrs)
    for svr in svrs:
        ips = domain2ip(svr['domain'])    # 新探测的服务器ips
        ips = list(set(ips).union(set(svr['ips'])))   # 新与旧ip地址求和
        print str(datetime.now()), svr['domain'],' whois ips detecting'
        print ips
        insert_db(svr['domain'], ips)
        svr_count -= 1
        print str(svr_count), " domains remaining"


if __name__ == '__main__':

    schedule.every(3).hours.do(get_svr_ip)  # 3小时循环

    while True:
        schedule.run_pending()
        time.sleep(1)