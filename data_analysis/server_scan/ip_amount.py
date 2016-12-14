# encoding:utf-8
"""
To analyze the delay variation of sever
"""

from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


def get_db():
    """
    获取数据库
    :return
    """
    client = MongoClient('localhost', 27017)
    db = client['whois_sever_analysis']
    return db


def get_ip_level(level='1'):

    ips = []
    db = get_db()
    col = db['svr_source']
    ip = col.find({'level':level},{'_id':0,'ips':1})
    for i in ip:
        ips.append(len(i['ips']))

    return ips


def formate_data(ips):
    """
    格式化输入数据
    :param ips:
    :return:
    """
    c = Counter()
    x_label = []
    y = []

    for ip in ips:
        c[ip] += 1

    for i in c:
        if i:
            x_label.append(i)
            y.append(c[i])
    x = np.arange(len(x_label))
    print x_label
    print y
    return x,y,x_label



def draw():




    fig = plt.figure(1, figsize=(9, 4.5), dpi=75)
    left = 0.09  # the left side of the subplots of the figure
    right = 0.96  # the right side of the subplots of the figure
    bottom = 0.13  # the bottom of the subplots of the figure
    top = 0.93  # the top of the subplots of the figure
    wspace = 0.25  # the amount of width reserved for blank space between subplots
    hspace = 0.2  # the amount of height reserved for white space between subplots
    plt.subplots_adjust(left, bottom, right, top, wspace, hspace)

    width = 0.5

    fig.add_subplot(121)
    ips = get_ip_level('1')
    x, y, x_label = formate_data(ips)
    plt.bar(x,y, width,align='center')
    x_min, x_max = x.min(), x.max()
    plt.xlim(x_min - 1, x_max + 1)
    plt.xticks(x, x_label)
    plt.ylabel('Number of WHOIS servers')
    plt.xlabel('WHOIS server contains the IP number')

    fig.add_subplot(122)
    ips = get_ip_level('2')
    x, y, x_label = formate_data(ips)
    plt.bar(x, y, width, align='center')
    x_min, x_max = x.min(), x.max()
    plt.xlim(x_min - 1, x_max + 1)
    plt.xticks(x, x_label)
    plt.ylabel('Number of WHOIS servers')
    plt.xlabel('WHOIS server contains the IP number')


    plt.savefig('../graph/ip_amount.png', dpi=75)
    plt.show()


if __name__ == '__main__':

    draw()
