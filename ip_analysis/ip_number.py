# encoding:utf-8

"""
服务器解析的IP数量的统计
1. 各个服务器解析出IP数量分布
2. 总共解析出的IP集
3. 各个IP表示的服务器数量分布，存在一对多的情况
@作者：程亚楠
@更新时间：2017.6.1
@创建时间：2017.3.1

"""

from collections import Counter
from db_manage import get_col
import matplotlib.pyplot as plt
import numpy as np


def get_svr_ip():
    """
    获取所有域名和ip
    :return:
    """

    col = get_col('com_svr')
    svr_ips = col.find({},{'_id': 0, 'ips': 1, 'domain': 1})
    return svr_ips


def ip_number_distribution(svr_ips):
    """
    WHOIS服务器解析ip数量分布统计
    :param svr_ips:  记录集合
    """
    c = Counter()
    for i in svr_ips:
        ip_count = len(i['ips'])  # 域名解析IP的数量

        # if ip_count >= 2:
            # print i['domain'], ip_count,i['ips']  # 输出IP数量大于1的服务器
            # print ','.join(i['ips'])

        c[ip_count] += 1  # 求IP数量的分布

    print "IP numbers|","|WHOIS server numbers"
    for i in c:
        print i, c[i]
    return c


def ip_count(svr_ips):
    """
    总共ip数量统计
    @todo:应该求iP集，而不是独立IP
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
    print "IP总数： ", len(ips)
    return ips


def draw_domain_ip(c):
    x_labels = []
    y_labels = []
    for i in c:
        x_labels.append(i)
        y_labels.append(c[i])

    fig = plt.figure(1, figsize=(7, 5.2), dpi=75)

    x = np.arange(len(x_labels))
    ax = fig.add_subplot(111)
    plt.bar(x, y_labels,align='center')
    plt.xticks(x, x_labels)
    plt.grid(True)

    plt.xlabel('The number of a WHOIS server domain resolves to IP')
    plt.ylabel('The number of WHOIS server domain')
    plt.savefig('./graph/ip_svr_num.png', dpi=75)
    plt.show()


def draw_ip_domain(c):

    c = c.most_common(10)
    x_labels = []
    y_labels = []
    for i in c:
        x_labels.append(i[0])
        y_labels.append(i[1])

    fig = plt.figure(1, figsize=(7, 5.2), dpi=75)

    left = 0.12  # the left side of the subplots of the figure
    right = 0.96  # the right side of the subplots of the figure
    bottom = 0.2  # the bottom of the subplots of the figure
    top = 0.93  # the top of the subplots of the figure
    wspace = 0.2  # the amount of width reserved for blank space between subplots
    hspace = 0.2  # the amount of height reserved for white space between subplots
    plt.subplots_adjust(left, bottom, right, top, wspace, hspace)

    x = np.arange(len(x_labels))
    ax = fig.add_subplot(111)
    plt.bar(x, y_labels)
    plt.xticks(x, x_labels)
    ax.set_xticklabels(x_labels, rotation=25)
    # plt.grid(True)
    plt.gca().yaxis.grid(True)  # 只显示y轴
    #
    plt.xlabel('The number of a WHOIS server domain resolves to IP')
    plt.ylabel('The number of WHOIS server domain')
    plt.savefig('./graph/ip_domain.png', dpi=75)
    plt.show()


def ip_svr_number(svr_ips):
    """
    ip所负责WHOIS服务器的分布
    :param svr_ips:

    """
    c = Counter()
    for i in svr_ips:
        if len(i['ips']) == 1:
            c[i['ips'][0]] += 1

    for i in c:
        print i, c[i]
    return c

if __name__ == '__main__':


    svr_ips = get_svr_ip()
    svr_ips_dist = svr_ips.clone()
    c = ip_number_distribution(svr_ips_dist)   # 服务器解析IP数量分布
    # draw_domain_ip(c)
    ip_numbers = svr_ips.clone()
    ip_count(ip_numbers)   # IP集合总数
    c = ip_svr_number(svr_ips)
    # draw_ip_domain(c)
