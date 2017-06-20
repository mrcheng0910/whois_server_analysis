# encoding:utf8

"""
发送不存在的域名到各个服务器，获取服务器返回的信息
"""

import time
import sys
import random

from whois_connect import GetWhoisInfo
from database import DataBase

reload(sys)
sys.setdefaultencoding('utf-8')

Table = 'HJ.not_found'


def main1():

    d_srv = []
    fp = open('detected.txt','r')
    for i in fp:
        d_srv.append(i.strip())
    fp.close()




    domain = 'adfdfsfadfsf.com'
    fp_srvs = open('srv_ranking.txt', 'r')
    srvs = []
    for i in fp_srvs:
        srvs.append(i.split(' ')[0].strip())

    fp_srvs.close()

    srvs = list(set(srvs)-set(d_srv))

    print '剩余探测服务器数量：',len(srvs)
    DB = DataBase()
    DB.db_connect()
    DB.execute_no_return("USE HJ")

    random.shuffle(srvs)


    for i in srvs:
        fp_a = open('detected.txt', 'a')
        d = GetWhoisInfo(domain, i.strip()).get()
        d = d.replace("\\", "")
        d = d.replace("'", "\\'")
        d = d.replace('"', '\\"')
        SQL = """INSERT INTO {table} SET `whois_srv` = '{w}' ,`details` = '{d}' """.format(
            table=Table, w=i, d=d)
        DB.execute_no_return(SQL)
        DB.db_commit()
        fp_a.write(i+'\n')
        fp_a.close()
        print '探测完成：', i
        time.sleep(10)

    DB.db_commit()
    DB.db_close()


if __name__ == '__main__':

    main1()