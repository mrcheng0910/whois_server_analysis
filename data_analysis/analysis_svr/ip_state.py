# encoding:utf-8

"""
统计分析IP的状态，该数据来源于长期针对IP的扫描
1. 发现是否有部分WHOIS服务器定期关机，无法提供查询服务；
2. 发现部分服务器提供查询性能不稳定
3. 统计长期关闭或者开放的IP

@注意：
1. 本地网络对探测的影响
2. 数据库中的时间为UTC+8，分析使用时间为UTC时间

@更新时间:2017年3月21日
针对新的扫描方法，进行数据统计分析

@更新时间：2017年2月28日
1. 优化代码

@创建时间：2017年2月15日

"""

from collections import Counter
from collections import defaultdict
import copy

import matplotlib.pyplot as plt
import numpy as np
# custom function
from db_manage import get_col
from localtime_to_utc import local2utc


def get_ip_state():
    """
    所有IP的长期探测情况
    """
    col = get_col('ip_scan_result_socket1')
    ip_state = col.find({})
    return ip_state


def classify_ip_state():
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
            if flag:
                up_ips.append(i)  # 关闭状态
            else:
                down_ips.append(i)   # 开放状态

    return diff_ips, up_ips, down_ips


def state_count(ips, show_flag=False):
    """
    ip状态计数
    :param ips:
    :return:
    """

    col = get_col('ip_scan_result_socket1')
    for ip in ips:
        scan_info = col.find({'ip': ip})
        c = Counter()
        for i in scan_info:
            if show_flag:
                print i['ip'],
                print i['state'],
                print local2utc(i['detected_time'])
            c[i['state']] += 1

        print ip, c[True], c[False]



def draw_graph():
    """
    绘制站点的域名解析数据，包括各个簇的域名个数,cname个数，ip个数等
    :param domain_data: 字典，各个属性的数量
    :return:
    """
    # domain_count = domain_data['domain_count']
    # cname_count = domain_data['cname_count']
    # ip_count = domain_data['ip_count']
    # N = len(domain_count)
    # ind = np.arange(1,N+1)
    # width = 0.7
    # plt.figure(1, figsize=(8, 6))
    # p1 = plt.bar(ind, domain_count, width, align='center',color='r',bottom=[x+y for x, y in zip(ip_count, cname_count)])
    # p2 = plt.bar(ind, cname_count, width, color='y',align='center',bottom=ip_count)
    # p3 = plt.bar(ind,ip_count,width,color='c',align='center')
    # x居中设置
    # x_min, x_max = ind.min(), ind.max()
    # plt.xlim(x_min - 1, x_max + 1)
    # plt.ylabel('the numbers')
    # plt.xlabel('sequence number')
    # plt.xticks(np.arange(1, N+1, 3))
    # plt.yticks()
    # 设置legend
    # plt.legend((p1[0], p2[0],p3[0]), ('Domain', 'CNAME', 'IP'),fontsize='11')

    # plt.savefig('./graph/' + "domain_hist.png", dpi=75)
    # plt.show()

    x = np.linspace(0, 10, 500)
    dashes = [10, 5, 100, 5]  # 10 points on, 5 off, 100 on, 5 off

    fig, ax = plt.subplots()
    line1, = ax.plot(x, np.sin(x), '--', linewidth=2,
                     label='Dashes set retroactively')
    line1.set_dashes(dashes)

    line2, = ax.plot(x, -1 * np.sin(x), dashes=[30, 5, 10, 5],
                     label='Dashes set proactively')

    ax.legend(loc='lower right')
    plt.show()


if __name__ == '__main__':

    diff_ips, up_ips, down_ips = classify_ip_state()
    print 'IP总数:', len(down_ips)+ len(up_ips)+len(diff_ips),
    print '关闭:', len(down_ips),
    print '开放:', len(up_ips),
    print '不稳定:', len(diff_ips)
    print '状态统计'
    state_count(down_ips)
    # state_count(up_ips)
    # state_count(down_ips)
    # draw_graph()

