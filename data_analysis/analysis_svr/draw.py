# encoding:utf-8

"""
统计分析IP的状态，该数据来源于长期针对IP的扫描
1. 发现是否有部分WHOIS服务器定期关机，无法提供查询服务；
2. 发现部分服务器提供查询性能不稳定
3. 统计长期关闭或者开放的IP

@创建时间：2017年2月15日

"""

from collections import defaultdict
import copy

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



def draw_mean_graph(ip_duration):
    """
    绘制服务器的端口平均延迟时间
    :param ip_duration: 
    :return: 
    """
    up_x = []
    mean_y = []
    for i in ip_duration:
        up_x.append(i['ip'])
        mean_y.append(i['mean'])

    x = np.arange(len(up_x))

    # 均值
    fig = plt.figure(1,figsize=(8.5, 5),dpi=75)
    ax = fig.add_subplot(111)
    mean = np.mean(mean_y)
    plt.plot(x, mean_y, 'o')
    plt.plot(x,[mean]*len(x), '.-')

    x_min, x_max = x.min(), x.max()
    plt.xlim(x_min - 1, x_max + 1)
    # ax.set_xticks([])  # x坐标轴设置为空
    plt.annotate('mean:' + str(round(mean, 2)),
                 xy=(43, mean),
                 xytext=(4, mean + 1),
                 arrowprops=dict(facecolor='black', shrink=0.03)
                 )
    plt.xlabel('the Sequence of IPs')
    plt.ylabel('Latency(senconds)')

    plt.savefig( "./graph/up_mean.png", dpi=75)
    plt.show()


def draw_var_graph(ip_duration):

    up_x = []
    var_y = []
    for i in ip_duration:
        up_x.append(i['ip'])
        var_y.append(i['var'])

    x = np.arange(len(up_x))

    # 方差
    fig = plt.figure(1,figsize=(8.5, 5),dpi=75)
    fig.add_subplot(111)
    mean = np.mean(var_y)
    plt.plot(x, var_y, 'o')
    plt.plot(x,[mean]*len(x), '.-')

    x_min, x_max = x.min(), x.max()
    plt.xlim(x_min - 1, x_max + 1)
    plt.annotate('mean:' + str(round(mean, 2)),
                 xy=(30, mean),
                 xytext=(40, mean+4),
                 arrowprops=dict(facecolor='black', shrink=0.03)
                 )
    plt.xlabel('the Sequence of IPs')
    plt.ylabel('Latency(s)')

    plt.savefig( "./graph/up_var.png", dpi=75)
    plt.show()


def cal_time(ip, show_flag=False):

    during_time_list = []
    col = get_col('ip_scan_result_socket1')
    scan_info = col.find({'ip': ip, 'state': True})
    for i in scan_info:
        during_time_list.append(i['during_time'])

    if show_flag:
        print ip, np.mean(during_time_list), np.var(during_time_list,ddof=1)

    return {'ip': ip,
            'mean': np.mean(during_time_list),
            'var': np.var(during_time_list, ddof=1)
            }


def main():
    """
    主函数
    """
    ip_duration = []
    diff_ips, up_ips, down_ips = classify_ip_state()
    for i in up_ips:
        print i
    # ips = copy.deepcopy(diff_ips)
    # for ip in ips:
    #     ip_duration.append(cal_time(ip))

    # 绘制
    # draw_mean_graph(ip_duration)
    # draw_var_graph(ip_duration)


if __name__ == '__main__':

    main()

