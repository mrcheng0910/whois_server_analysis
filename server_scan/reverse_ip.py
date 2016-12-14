#!/usr/bin/python
# encoding:utf-8
"""
用来获取whois域名的IP地址
"""
from datetime import datetime
import dns.resolver
from db_manage import get_db


def domain2ip(domain):
    """
    域名解析为IP列表
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

    db = get_db()
    col = db['svr_source']
    col.update({'domain':domain},{'$set':{'ips':ips}},False,True)  # 修改某字段


def get_svr():
    svrs = []
    db =get_db()
    col = db['svr_source']
    svr_cur = col.find({},{'_id':0,'domain':1,'ips':1})
    for svr in svr_cur:
        print svr
        svrs.append(svr)

    return svrs


def get_svr_ip():
    """
    获取服务器的IP地址，并与已有ip比对,最后更新数据库
    """
    import random

    svrs = get_svr()
    random.shuffle(svrs)  # 将列表进行随机
    for svr in svrs:
        ips = domain2ip(svr['domain'])
        ips = list(set(ips).union(set(svr['ips'])))
        print str(datetime.now()), svr['domain'],'服务器探测'
        print ips
        insert_db(svr['domain'],ips)



if __name__== '__main__':
    # get_svr_ip()
    get_svr_ip()