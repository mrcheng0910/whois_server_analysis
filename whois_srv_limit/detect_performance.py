# encoding:utf8

"""
"""

import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from whois_connect import GetWhoisInfo
from database import DataBase

PATH = 'Data/domain/'
DOMAIN_EXAMPLE = 'example.com'


def main(filename,Table,sleep_time):
    """主流程"""
    DB = DataBase()
    DB.db_connect()
    DB.execute_no_return("USE HJ")
    # fileList = os.listdir(PATH)
    # for filename in fileList:
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
        SQL = """INSERT INTO {table} SET `whois_srv` = '{w}' ,`whois_ip` = '{i}' ,`domain` = '{dn}' ,`search_time` = {t} ,`details` = '{d}' """.format(
            table=Table, w=whoissrv, i=whoisip, t=T, d=str(D), dn=domain.strip()
        )
        DB.execute_no_return(SQL)
        DB.db_commit()
        time.sleep(sleep_time)
    f.close()
    DB.db_commit()
    DB.db_close()


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

    filename = sys.argv[1]
    db_name = sys.argv[2]
    sleep_time = int(sys.argv[3])
    Table = 'HJ.'
    Table = Table + db_name
    while 1:
        main(filename, Table, sleep_time)