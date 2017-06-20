# encoding:utf-8

"""
统计分析WHOIS服务器IP的稳定性

@创建时间：2017年4月1日

"""

from collections import Counter
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from pandas import Series
# custom function
from db_manage import get_col


def get_ip_state():
    """
    所有IP的长期探测情况
    """
    col = get_col('ip_scan_result_socket1')
    ip_state = col.find({})
    return ip_state


def read_file_ip(file_name='ip_result_bj.txt'):
    """
    读取文件中所有原始探测数据
    :param file_name: 
    :return: 
    """
    ip_state = []
    fp = open(file_name, 'r')

    for i in fp:
        ip_split = i.split('\t')
        ip, state, during_time = ip_split[0],ip_split[1],ip_split[2]
        ip_state.append({
            'ip': ip,
            'state': state == 'True',
            'during_time': float(during_time)
        })

    fp.close()
    return ip_state


def classify_ip_state():
    """
    获取状态不一致的ip列表,开放ip列表，关闭ip列表
    :return:
        diff_ips：状态不一致ips
        up_ips：开放ips
        down_ips: 关闭ips
    """
    bj_ip_state = read_file_ip('./distribution_ip/ip_result_bj.txt')
    sh_ip_state = read_file_ip('./distribution_ip/ip_result_sh.txt')
    hn_ip_state = read_file_ip('./distribution_ip/ip_result_hn.txt')
    dis_ip_state = bj_ip_state+sh_ip_state+hn_ip_state
    ip_state = get_ip_state()
    ip_up = []
    ips = []
    during_time = []
    dl = defaultdict(list)

    for i in ip_state:
        dl[i['ip']].append(i['state'])

        # 若连接成功则记录延迟时间
        if i['state']:
            ips.append(i['ip'])
            during_time.append(i['during_time'])

    for i in dis_ip_state:
        dl[i['ip']].append(i['state'])

        # 若连接成功则记录延迟时间
        if i['state']:
            ips.append(i['ip'])
            during_time.append(i['during_time'])

    data_series = Series(during_time, index=ips)  # series数据

    for i in dl:
        up_count, down_count = Counter(dl[i])[True], Counter(dl[i])[False]
        total_count = up_count + down_count
        ip_up.append([i, round(up_count/float(total_count), 2)])

    return ip_up, data_series


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

    ip_up,_ = classify_ip_state()  # 获取IP的状态分布
    draw_graph(ip_up)   # 绘制直方图

    # 统计完全关闭和完全开放的IP数量
    ip_up,_ = classify_ip_state()
    total = len(ip_up)
    up = 0
    down = 0
    for i in ip_up:
        if i[1] >= .9:
            up += 1
        elif i[1] <= 0.1:
            down += 1

    print up/float(total)
    print down/float(total)


