# encoding:utf-8

"""
服务器负责域名的数量分布情况，并且绘图
"""

import matplotlib.pyplot as plt
import numpy as np
from  collections import Counter

def read_file_ip():
    """
    读取文件中所有原始探测数据
    :param file_name: 
    :return: 
    """

    srv_domain_num = {}
    total_domain = 0
    fp = open('dist_of_domain.txt', 'r')

    for i in fp:
        svr_split = i.split('\t')
        srv, count = svr_split[0], svr_split[1]
        srv_domain_num[srv] = int(count.strip())
        total_domain += int(count.strip())
    fp.close()

    srv_counter = Counter(srv_domain_num)


    for i,j in srv_counter.most_common(15):
        print i,'\t',j

    print total_domain



def draw_graph():
    """
    绘制站点的域名解析数据，包括各个簇的域名个数,cname个数，ip个数等
    :param domain_data: 字典，各个属性的数量
    :return:
    """

    x_label = []
    y = []
    svr_count = read_file_ip()

    for i in svr_count:
        x_label.append(i['svr'])
        y.append(i['count'])
    x = np.arange(len(x_label))

    for i in x_label[:10]:
        print i

    fig = plt.figure(1, figsize=(8, 6), dpi=75)

    left = 0.12  # the left side of the subplots of the figure
    right = 0.96  # the right side of the subplots of the figure
    bottom = 0.5  # the bottom of the subplots of the figure
    top = 0.93  # the top of the subplots of the figure
    wspace = 0.2  # the amount of width reserved for blank space between subplots
    hspace = 0.2  # the amount of height reserved for white space between subplots
    plt.subplots_adjust(left, bottom, right, top, wspace, hspace)

    ax = fig.add_subplot(111)
    plt.bar(x[:10], y[:10])
    # x_min, x_max = x[:10].min(), x[:10].max()
    # plt.xlim(x_min - 1, x_max + 1)
    plt.xticks(x[:10], x_label[:10])
    # ax.set_xticks(x[:10])
    ax.set_xticklabels(x_label[:10], rotation=63)
    plt.grid(True)

    plt.xlabel('WHOIS server name')
    plt.ylabel('COM Domain number')
    plt.savefig('./graph/svr_dm_dist.png',dpi=75)
    plt.show()


if __name__ == '__main__':
    read_file_ip()


    # draw_graph()