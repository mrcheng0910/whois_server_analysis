# encoding:utf-8

"""
统计分析所有服务器的连接事件，包括均值、方差和均值-方差
@创建时间：2017年2月15日

"""

from collections import defaultdict
import copy

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

    ips = []
    during_time = []

    # 获取所有ip的状态（去重）
    for i in ip_status_set:
        ds[i['ip']].add(i['state'])
        if i['state']:
            ips.append(i['ip'])
            during_time.append(i['during_time'])

    data_series = Series(during_time, index=ips)  # series数据

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

    return diff_ips, up_ips, down_ips, data_series


def draw(result):

    x = []
    mean_coor = []
    var_coor = []
    for i in result:
        x.append(i['ip'])
        mean_coor.append(i['mean'])
        var_coor.append(i['var'])

    fig = plt.figure(1, figsize=(12, 5), dpi=75)

    left = 0.09  # the left side of the subplots of the figure
    right = 0.96  # the right side of the subplots of the figure
    bottom = 0.2  # the bottom of the subplots of the figure
    top = 0.93  # the top of the subplots of the figure
    wspace = 0.2  # the amount of width reserved for blank space between subplots
    hspace = 0.2  # the amount of height reserved for white space between subplots
    plt.subplots_adjust(left, bottom, right, top, wspace, hspace)


    # 平均值分布
    fig.add_subplot(131)
    mean_mean = np.mean(mean_coor)
    # plt.plot(np.arange(len(x)), mean_coor,'o')
    plt.scatter(np.arange(len(x)),mean_coor)
    plt.plot(np.arange(len(x)), [mean_mean] * len(x), 'r--',linewidth=3)

    plt.xlim(0, len(x))
    plt.ylim(0,max(mean_coor) + 0.05)
    # ax.set_xticks([])  # x坐标轴设置为空
    plt.annotate('mean:' + str(round(mean_mean, 2)),
                 xy=(43, mean_mean),
                 xytext=(4, mean_mean + 1),
                 arrowprops=dict(facecolor='black', shrink=0.03)
                 )
    plt.xlabel('the Sequence of IPs')
    plt.ylabel('Latency(senconds)')

    fig.add_subplot(132)
    var_mean = np.mean(var_coor)
    # plt.plot(np.arange(len(x)), var_coor, 'o')
    plt.scatter(np.arange(len(x)),var_coor)
    plt.plot(np.arange(len(x)), [var_mean] * len(x), 'g--',linewidth=3)

    plt.xlim(0, len(x))
    plt.ylim(0, max(var_coor))
    plt.annotate('mean:' + str(round(var_mean, 2)),
                 xy=(30, var_mean),
                 xytext=(40, var_mean + 4),
                 arrowprops=dict(facecolor='black', shrink=0.03)
                 )
    plt.xlabel('the Sequence of IPs')
    plt.ylabel('Latency(s)')

    fig.add_subplot(133)
    # plt.plot(mean_coor,var_coor,'o')
    plt.plot([mean_mean]*len(var_coor),var_coor,'r.-')
    plt.plot(mean_coor,[var_mean]*len(mean_coor),'g.-')
    plt.scatter(mean_coor,var_coor)
    x_min, x_max = min(mean_coor), max(mean_coor)
    y_min, y_max = min(var_coor), max(var_coor)
    plt.xlim(x_min, x_max + 0.1)
    plt.ylim(y_min, y_max + 0.05)

    plt.xlabel('connection time ')
    plt.ylabel('connection var')

    plt.savefig("./graph/up_mean1.png", dpi=75)
    plt.show()


def cal(ips,data_series):
    import math
    ip_cal_result = []
    for ip in ips:
        mean = np.mean(data_series[ip])
        var = np.var(data_series[ip], ddof=1)
        if math.isnan(var):
            continue
        ip_cal_result.append({
            'ip': ip,
            'mean': mean,
            'var': var
        })
    return ip_cal_result


def main():
    """
    主函数
    """
    ip_duration = []
    diff_ips, up_ips, down_ips,data_series = classify_ip_state()
    ip_cal_result = cal(diff_ips+up_ips,data_series)
    draw(ip_cal_result)


if __name__ == '__main__':

    main()

