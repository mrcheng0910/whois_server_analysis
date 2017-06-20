# encoding:utf-8

"""
统计分析所有服务器的连接事件，包括均值、方差和均值-方差
@创建时间：2017年2月15日

"""

import matplotlib.pyplot as plt
import numpy as np

# custom function
from ip_state_statistics import classify_ip_state


def draw1(ip_mean,ip_var):

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
    mean_mean = np.mean(ip_mean)
    plt.scatter(np.arange(len(ip_mean)), ip_mean)
    plt.plot(np.arange(len(ip_mean)), [mean_mean] * len(ip_mean), 'r--', linewidth=3)

    plt.xlim(0, len(ip_mean))
    plt.ylim(0, max(ip_mean) + 0.05)
    # ax.set_xticks([])  # x坐标轴设置为空
    plt.annotate('mean:' + str(round(mean_mean, 2)),
                 xy=(43, mean_mean),
                 xytext=(4, mean_mean + 1),
                 arrowprops=dict(facecolor='black', shrink=0.03)
                 )
    plt.xlabel('the Sequence of IPs')
    plt.ylabel('Latency(senconds)')

    fig.add_subplot(132)
    var_mean = np.mean(ip_var)
    plt.scatter(np.arange(len(ip_var)), ip_var)
    plt.plot(np.arange(len(ip_var)), [var_mean] * len(ip_var), 'g--', linewidth=3)
    plt.xlim(0, len(ip_var))
    plt.ylim(0, max(ip_var))
    plt.annotate('mean:' + str(round(var_mean, 2)),
                 xy=(30, var_mean),
                 xytext=(40, var_mean + 4),
                 arrowprops=dict(facecolor='black', shrink=0.03)
                 )
    plt.xlabel('the Sequence of IPs')
    plt.ylabel('Latency(s)')
    #
    fig.add_subplot(133)
    # # plt.plot(mean_coor,var_coor,'o')
    plt.plot([mean_mean] * len(ip_var), ip_var, 'r.-')
    plt.plot(ip_mean, [var_mean] * len(ip_mean), 'g.-')
    plt.scatter(ip_mean, ip_var)
    x_min, x_max = min(ip_mean), max(ip_mean)
    y_min, y_max = min(ip_var), max(ip_var)
    plt.xlim(x_min, x_max + 0.1)
    plt.ylim(y_min, y_max + 0.05)
    #
    # plt.xlabel('connection time ')
    # plt.ylabel('connection var')

    plt.savefig("./graph/up_mean1.png", dpi=75)
    plt.show()


def cal_mean_var():

    ip_mean = []
    ip_var = []
    up_ip, data_series = classify_ip_state()
    for ip in up_ip:
        if ip[1] >= 0.9:  # 稳定性大于0.9
            mean =  np.mean(data_series[ip[0]])
            ip_mean.append(mean)
            var = np.var(data_series[ip[0]],ddof=1)
            ip_var.append(var)

    return ip_mean, ip_var


def main():
    """
    主函数
    """
    ip_mean, ip_var = cal_mean_var()
    draw1(ip_mean,ip_var)



if __name__ == '__main__':

    main()

