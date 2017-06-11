# encoding:utf-8
"""
域名注册商所含有的域名服务器分布
"""

from fetch_reg_srv_data import update_reg_data
from collections import defaultdict
from collections import Counter
import pickle


def open_data():
    """
    打开原始注册商和服务器原始数据文件
    """
    reg_srv_data = pickle.load(open("registrar_srv_data.pkl", "r"))
    return reg_srv_data


def manage_data(reg_srv_data):
    reg_srvs = defaultdict(set)  # 注册商含有WHOIS服务器情况
    srv_regs = defaultdict(set)  # 服务器被注册商使用情况

    for i in reg_srv_data:
        # 注册商名称
        original_reg = i[0].strip()
        lower_reg = original_reg.lower()
        filter_reg = filter(str.isalnum, lower_reg)

        # 服务器
        lower_srv = i[1].strip().lower()

        reg_srvs[filter_reg].add(lower_srv)  # 注册商含有的WHOIS服务器情况
        srv_regs[lower_srv].add(filter_reg)  # 服务器被注册商使用情况

    return reg_srvs, srv_regs


def count_reg_srv(reg_srvs):
    """
    统计注册商含有的服务器数量
    """
    c = Counter()
    srv_amount = 0
    for i in reg_srvs:
        c[len(reg_srvs[i])] += 1

        # if len(reg_srvs[i]) == 3:
        #     print i
        #     print reg_srvs[i]

    print '注册商数量', 'WHOIS服务器数量'
    for i in c:
        srv_amount += c[i]
        print i, '\t', c[i]
    print srv_amount


def count_srv_reg(srv_regs):
    """
    统计服务器被注册商使用情况
    """
    c = Counter()
    for i in srv_regs:
        c[len(srv_regs[i])] += 1
        # if len(srv_regs[i]) == 377:
        #     print i, srv_regs[i]

    print '服务器被多少个注册商使用','这种情况的服务器数量'
    for i in c:
        print i,'\t', c[i]
    print len(srv_regs)


def srv_query_reg(srv_regs,srv = ""):
    """
    根据输入WHOIS服务器，查询与其对应的WHOIS服务器地址
    :param srvs:
    :return:
    """
    if srv == "":
        return

    return srv_regs[srv.strip().lower()]


def query_reg(srv_regs):
    """
    查询WHOIS服务器的Registrar名称
    """
    srvs = []
    fp = open('top_srv.txt','r')
    for i in fp:
        srvs.append(i.strip().split('\t')[0].strip())

    for i in srvs:
        print i
        regs = srv_query_reg(srv_regs,i)
        print len(regs)
        if i == 'whois.tucows.com':
            print regs


def main():

    # update_reg_data(end_tb=20)
    reg_srv_data = open_data()
    reg_srvs, srv_regs = manage_data(reg_srv_data)
    # count_reg_srv(reg_srvs)   # 统计分析
    count_srv_reg(srv_regs)

    # query_reg(srv_regs)


if __name__ == '__main__':
    main()




