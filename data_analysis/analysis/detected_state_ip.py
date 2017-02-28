# encoding:utf-8
"""
获取不同状态的IP集合
"""

import copy
from collections import defaultdict
from db_manage import get_col


def get_ip_state():
    """
    所有IP的长期探测情况
    """
    col = get_col('ip_scan_result1')
    ip_state = col.find({}, {'_id': 0, 'ip': 1, 'state': 1, 'detected_time': 1})
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
            if flag == 'down':
                down_ips.append(i)  # 关闭状态
            elif flag == 'up':
                up_ips.append(i)   # 开放状态

    return diff_ips, up_ips, down_ips


