# encoding:utf-8

import math
import os
import re
from datetime import datetime
from db_manage import get_open_ip,insert_net_state


def ping(ip, count = 10):

    res = os.popen("ping " + ip + " -c " + str(count))
    resLst = list(res)
    print resLst
    lossPattern = re.compile(r".+? ([\d\.]+)%")
    loss = 0
    for i in resLst:
        info = lossPattern.findall(i)
        if info:
            loss = float(info[0])
            break

    ttlPattern = re.compile(r'.+?ttl=(.+)')
    ttlLst = []
    for i in resLst:
        info = ttlPattern.findall(i)
        if info:
            ttlLst.append(int(info[0].split(' ')[0]))
    print ttlLst
    ttl_mean = sum(ttlLst)/len(ttlLst)
    print int(ttl_mean)
    timePattern = re.compile(r'.+?time=(.+) .*s')
    timeLst = []
    for i in resLst:
        info = timePattern.findall(i)
        if info:
            timeLst.append(float(info[0]))
    num = len(timeLst)
    if num == 0:
        return loss, 100, 0
    mean = sum(timeLst) / num
    tmp = 0
    for i in timeLst:
        tmp += (i - mean) * (i - mean)
    if num != 1:
        variance = math.sqrt(tmp) / (num-1)
    else:
        variance = 0
    return loss, mean, variance,ttl_mean


def ip_state():
    """
    Detect ip net state
    :return:
    """
    ips = get_open_ip()
    for ip in ips:
        try:
            loss, delay,var, ttl_mean = ping(ip)
        except:
            loss, delay, var, ttl_mean = 100, 0, 0, 0   # 异常情况

        insert_net_state({
            'ip':ip,
            'loss':loss,
            'delay':delay,
            'var':var,
            'ttl':ttl_mean,
            'detected_time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })


if __name__ == "__main__":

    ip_state()

	
