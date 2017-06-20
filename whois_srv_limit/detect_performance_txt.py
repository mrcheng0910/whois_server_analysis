# encoding:utf8

"""
"""

import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from whois_connect import GetWhoisInfo

PATH = 'Data/domain/'
DOMAIN_EXAMPLE = 'example.com'


def main(filename,sleep_time):
    """主流程"""
    whoissrv = filename.split('-', 1)[1].strip()[:-4]
    whoisip = filename.split('-', 1)[0].strip()
    print whoissrv, whoisip
    f = open(str(PATH + filename), 'r')
    domainList = f.readlines()
    if domainList == []:
        domainList.append(DOMAIN_EXAMPLE)
    for domain in domainList:
        T, D = TestWhoisSrv(domain.strip(), whoisip)
        if D is None:
            D = ''
        if len(D) > 5:
            # print D
            D = D.replace("\\", "")
            D = D.replace("'", "\\'")
            D = D.replace('"', '\\"')
        time.sleep(sleep_time)
    f.close()


def TestWhoisSrv(domain, whois_srv):
    """
    测试whois服务器性能
    :param domain: 域名
    :param whois_srv: whois服务器地址 ip/whois
    :return: T - 获取此条记录的时间 
             D - 获取的结果
    """
    start = time.time()
    try:
        D = GetWhoisInfo(domain, whois_srv).get()  # 获取
    except Exception as e:
        D = str(e)
    end = time.time()
    T = end - start
    return T, D


if __name__ == '__main__':

    sleep_time = int(sys.argv[1])
    filename='104.238.108.9-whois.wildwestdomains.com.txt'
    while 1:
        main(filename, sleep_time)