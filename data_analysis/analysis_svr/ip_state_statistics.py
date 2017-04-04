# encoding:utf-8

"""
统计分析WHOIS服务器IP的稳定性

@创建时间：2017年4月1日

"""

from collections import Counter
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
# custom function
from db_manage import get_col


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

    ip_state = get_ip_state()
    ip_up = []

    dl = defaultdict(list)

    for i in ip_state:
        dl[i['ip']].append(i['state'])

    for i in dl:
        up, down = Counter(dl[i])[True], Counter(dl[i])[False]
        total = up + down
        ip_up.append([i, round(up/float(total),2)])

    return ip_up


def draw_graph(ip_up):
    """
    绘制站点的域名解析数据，包括各个簇的域名个数,cname个数，ip个数等
    :param domain_data: 字典，各个属性的数量
    :return:
    """

    ups = []
    for i in ip_up:
        ups.append(i[1])
    bins = np.arange(0, 1.1, 0.1)

    fig = plt.figure(1, figsize=(6, 5.5), dpi=75)
    fig.add_subplot(111)

    plt.hist(ups, bins, align='mid')
    plt.grid(True)
    plt.xlabel('WHOIS Server Stability')
    plt.ylabel('WHOIS Server IP Address Numbers')
    plt.savefig('./graph/whois_server_stability.png')
    plt.show()


if __name__ == '__main__':

    # ip_up = classify_ip_state()  # 获取IP的状态分布
    # draw_graph(ip_up)   # 绘制直方图

    # 统计完全关闭和完全开放的IP数量
    ip_up = classify_ip_state()
    up = 0
    down = 0
    for i in ip_up:
        if i[1] >= .9:
            up += 1
        elif i[1] <= 0.1:
            down += 1

    print up
    print down


