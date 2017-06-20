# encoding:utf-8

from collections import defaultdict,Counter
import matplotlib.pyplot as plt
import numpy as np


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
            'state': state == 'True'
        })

    fp.close()
    return ip_state


def classify_ip_state(file_name='ip_result_bj.txt'):
    """
    获取状态不一致的ip列表,开放ip列表，关闭ip列表
    :return:
        diff_ips：状态不一致ips
        up_ips：开放ips
        down_ips: 关闭ips
    """

    ip_state_bj = read_file_ip('ip_result_bj.txt')
    ip_state_sh = read_file_ip('ip_result_sh.txt')
    ip_state_hn = read_file_ip('ip_result_hn.txt')
    ip_state = ip_state_bj + ip_state_hn + ip_state_sh

    ip_up_down = []
    dl = defaultdict(list)

    for i in ip_state:
        dl[i['ip']].append(i['state'])

    for i in dl:
        up, down = Counter(dl[i])[True], Counter(dl[i])[False]
        total = up + down
        ip_up_down.append([i, round(up/float(total), 2), round(down/float(total), 2)])

    return ip_up_down


def draw_graph(ip_up_down):
    """
    绘制站点的域名解析数据，包括各个簇的域名个数,cname个数，ip个数等
    :param domain_data: 字典，各个属性的数量
    :return:
    """
    fig = plt.figure(1, figsize=(8, 4), dpi=75)

    fig.add_subplot(111)
    ups = []
    for i in ip_up_down:
        ups.append(i[1])

    bins = np.arange(0, 1.1, 0.1)
    counts, _, _ = plt.hist(ups, bins,align='mid')
    # plt.xlim(0, 1.05)
    # plt.xticks(np.arange(len(bins)), bins)
    # plt.set_xticks(bins)
    # plt.xlim(0, len(ups))
    # plt.ylim(0, 1.1)
    bin_centers = 0.5 * np.diff(bins) + bins[:-1]
    for count, x in zip(counts, bin_centers):
        # Label the raw counts
        plt.annotate(str(int(count)), xy=(x, 0), xycoords=('data', 'axes fraction'),
                    xytext=(0, -18), textcoords='offset points', va='top', ha='center')
    plt.grid(True)
    # plt.xlabel('the Sequence of IPs(%)')
    plt.ylabel('Up times(%)')
    plt.show()


if __name__ == '__main__':
    ip_up_down = classify_ip_state()
    print len(ip_up_down)
    draw_graph(ip_up_down)