# encoding:utf-8

"""

"""

from collections import Counter
from collections import defaultdict
import copy

# custom function
from db_manage import get_col
from localtime_to_utc import local2utc
from ip_state import classify_ip_state


def query_ip_domain(ip):
    """
    查询IP所对应的WHOIS服务器域名
    :param ip:
    :return:
    """
    svr_domain = set()
    col = get_col('com_svr')
    ip_domain = col.find({'ips':ip},{'_id':0,'domain':1})
    for i in ip_domain:
        svr_domain.add(i['domain'])

    return list(svr_domain)


if __name__ == '__main__':
    diff_ips, up_ips, down_ips = classify_ip_state()
    test = []
    print len(down_ips)
    for i in down_ips:
        print i,
        domain = query_ip_domain(i)
        print domain
        test.extend(domain)

    print len(test)
    print len(list(set(test)))
    print set(test)


