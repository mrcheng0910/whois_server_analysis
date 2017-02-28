#encoding: utf-8
"""
本地时间转换为utc时间
"""
import datetime

def local2utc(d, hours=-8):
    """
    将本地（中国）时间转换为UTC
    :param hours: 转换的时间
    :param d: 时间
    :return: 转换后的时间
    """
    local_time = datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
    utc_time = local_time + datetime.timedelta(hours=hours)  # utc时间
    return utc_time
