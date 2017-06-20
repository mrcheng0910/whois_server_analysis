# encoding: utf-8

"""
分析服务器whois.no-ip.com的IP情况
1. 长期关闭
2. 长期开放
3. 不稳定IP，有时开放有时关闭

@作者：程亚楠
@创建时间：2017.2.28

"""

from collections import Counter,defaultdict
from db_manage import get_col
from localtime_to_utc import local2utc
import matplotlib.pyplot as plt
import numpy as np

def get_no_ip():
    """
    获取各类状态的ip列表和数量
    :returns
        long_term_up_ips，长期开放ip
        instability_ips，不稳定ip
    """

    # 得到whois.no-ip.com的所有解析IP
    col = get_col('com_svr')
    ips = col.find({'domain': 'whois.no-ip.com'},{'_id': 0, 'ips': 1})
    ips = ips[0]['ips']    # to retrieve the whole ips of whois.no-ip.com server
    return ips


def get_ip_state():

    ips = get_no_ip()
    # 获取所有ip的状态扫描结果
    # down_ips = set()
    # up_ips = set()
    col = get_col('ip_scan_result_socket1')
    dl = defaultdict(list)
    for ip in ips:
        scan_info = col.find({'ip': ip})
        for i in scan_info:
            dl[i['ip']].append(i['state'])

    return dl


def cal_ip_state(dl):

    ip_up = []
    for i in dl:
        up_count, down_count = Counter(dl[i])[True], Counter(dl[i])[False]
        total_count = up_count + down_count
        ip_up.append([i, round(up_count/float(total_count), 2)])

    for i in ip_up:
        print i
    return ip_up


def draw(ip_up):

    fig = plt.figure(1, figsize=(7, 5), dpi=75)
    y = []
    for i in ip_up:
        y.append(i[1])
    # 平均值分布
    fig.add_subplot(111)
    plt.scatter(np.arange(len(y)), y)

    plt.savefig("./graph/no-ip.png", dpi=75)
    plt.show()


if __name__ == '__main__':

    dl = get_ip_state()
    ip_up = cal_ip_state(dl)
    draw(ip_up)