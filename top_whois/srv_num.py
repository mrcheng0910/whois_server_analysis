# encoding:utf-8
"""
从基础数据库表中，统计、保存服务器和域名数量
"""

from mysqldb import MySQL
from collections import Counter
import pickle


def get_srvs():
    """
    获取服务器和与之对应的域名数量
    """
    mysql = MySQL(HOST='172.29.152.249', USER='root', PASSWORD='platform')
    mysql.connect()
    mysql.select_db('top_whois_srv_com')
    srv_num = {}
    for table_num in xrange(1, 6):
        print 'table: ', str(table_num)

        sql = """SELECT sec_whois_server,count(*) FROM domain_whois_com_top_srv_{n} WHERE sec_whois_server!='' AND sec_whois_server!='0' AND sec_whois_server IS NOT NULL GROUP BY sec_whois_server""".format(n=table_num)
        registrar_data = mysql.execute_sql(sql)[0]

        for i in registrar_data:
            try:
                srv_num[i[0].lower()] += int(i[1])
            except:
                srv_num[i[0].lower()] = int(i[1])
    mysql.disconnect()

    return srv_num


def save_data(srv_num):
    pickle.dump(srv_num, open("srv_num.pkl", "w"))


def open_data():
    srv_num = pickle.load(open("srv_num.pkl", "r"))
    return srv_num


def count_reg_srv(srv_num):
    """
    统计注册商含有的服务器数量
    """
    top_srv = 10
    top_srv_domain = 0  # top N 中服务器含有的域名数量
    c = Counter(srv_num)

    print 'WHOIS服务器名称', '\t', '域名数量'
    for i in c.most_common(top_srv):
        print i[0], '\t', i[1]
        top_srv_domain += i[1]

    total_domain_num = sum(c.values())
    print '域名总数: ', total_domain_num
    print 'top',top_srv,'域名数量: ', top_srv_domain
    print 'top/total: ', top_srv_domain/float(total_domain_num)
    print '服务器总数：', len(c)


def srv_list(srv_num):
    """
    返回所有服务器名称列表
    """
    return srv_num.keys()


def main():
    srv_num = get_srvs()  # 从数据库中获取所有服务器名称和域名数量
    save_data(srv_num)  # 持久性存储
    srv_num = open_data()  # 从文件中读取数据
    count_reg_srv(srv_num)   # 统计分析
    # srvs = srv_list(srv_num)
    # for i in srvs:
    #     print i


if __name__ == '__main__':
    main()
