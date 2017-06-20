# encoding:utf-8

"""
获取ip所关联的所有WHOIS服务器地址
"""

from db_manage import get_col
import pandas as pd

IP = '54.169.3.183'
file_name = IP+'_srvs.txt'
def get_svrs():

    fp = open(file_name,'w')
    col = get_col('com_svr')
    srvs = col.find({'ips':IP},{'_id': 0,  'domain': 1})
    for i in srvs:
        print i['domain']
        fp.write(i['domain'] + '\n')

    fp.close()


def manage_srv():
    srvs = []
    fp = open(file_name,'r')
    for i in fp:
        srvs.append(i.strip().split('.')[1])


    return srvs

def open_com_reg_raw():
    """
    读取com报告中的注册商和注册商拥有的域名数据
    """
    # 读取com报告中的数据
    com_srvs = []
    srv_num = {}
    reg_df = pd.read_csv('../registrar_analysis/com_registrar_num.csv', names=['reg_name', 'num'])
    for i in reg_df.values:
        original_reg = i[0].strip()
        lower_reg = original_reg.lower()
        filter_reg = filter(str.isalnum, lower_reg)

        com_srvs.append(filter_reg)
        srv_num[filter_reg] = i[1]
    return com_srvs,srv_num


def vs_svr(srvs,com_srvs):
    same_srvs = []
    for i in srvs:
        for j in com_srvs:
            if i in j:
                print i
                same_srvs.append(j)

    print len(same_srvs)
    return same_srvs


def number(same_srvs,srv_num):

    total = 0
    for i in same_srvs:
        total += srv_num[i]

    print total


if __name__ == '__main__':
    get_svrs()
    srvs = manage_srv()
    com_srvs,srv_num = open_com_reg_raw()
    same_srvs = vs_svr(srvs,com_srvs)
    number(same_srvs,srv_num)