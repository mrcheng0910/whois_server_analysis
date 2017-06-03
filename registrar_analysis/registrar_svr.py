# encoding:utf-8
"""
域名注册商所含有的域名服务器分布
"""

from mysqldb import MySQL
from collections import defaultdict
from collections import Counter
import pickle


def registrar_srvs():
    """
    统计域名注册商的别名，即在WHOIS信息中，域名注册商的名字出现多少种样式
    包括大小写、名称中间有标点、名称后有标点
    :return:
    """
    mysql = MySQL(HOST='172.29.152.249', USER='root', PASSWORD='platform')
    mysql.connect()
    mysql.select_db('domain_whois')

    reg_srvs = defaultdict(set)   # 注册商含有WHOIS服务器情况
    srv_regs = defaultdict(set)   # 服务器被注册商使用情况

    for table_num in xrange(1, 5):
        print 'table: ', str(table_num)
        sql = """SELECT sponsoring_registrar, sec_whois_server FROM domain_whois_{n} WHERE tld='com' AND sponsoring_registrar!='' AND sec_whois_server!='' GROUP BY sponsoring_registrar,sec_whois_server""".format(n=table_num)
        registrar_data = mysql.execute_sql(sql)[0]

        for i in registrar_data:
            # 注册商名称
            original_reg = i[0].strip()
            lower_reg = original_reg.lower()
            filter_reg = filter(str.isalnum, lower_reg)

            # 服务器
            lower_srv = i[1].strip().lower()

            reg_srvs[filter_reg].add(lower_srv)  # 注册商含有的WHOIS服务器情况
            srv_regs[lower_srv].add(filter_reg)   # 服务器被注册商使用情况

    mysql.disconnect()

    return reg_srvs, srv_regs


def save_data(reg_srvs,srv_regs):
    pickle.dump(reg_srvs, open("reg_srvs.pkl", "w"))
    pickle.dump(srv_regs, open("srv_regs.pkl", "w"))


def open_data():
    # 从 reg_alias.txt 中读取并恢复 obj 对象
    reg_srvs = pickle.load(open("reg_srvs.pkl", "r"))
    srv_regs = pickle.load(open("srv_regs.pkl", "r"))
    return reg_srvs, srv_regs


def count_reg_srv(reg_srvs):
    """
    统计注册商含有的服务器数量
    """
    c = Counter()
    srv_amount = 0
    for i in reg_srvs:
        c[len(reg_srvs[i])] += 1
        # if len(reg_srvs[i]) == 3:
        #     print i,reg_srvs[i]

    print '注册商数量', 'WHOIS服务器数量'
    for i in c:
        srv_amount += c[i]
        print i, '\t', c[i]
    print srv_amount


def count_srv_reg(srv_regs):
    """
    统计服务器被注册商使用情况
    """
    c = Counter()
    for i in srv_regs:
        c[len(srv_regs[i])] += 1
        # print i, srv_regs[i]
        # if len(srv_regs[i]) == 759:
        #     print i, srv_regs[i]

    print 'WHOIS服务器','注册商'
    for i in c:
        print i, c[i]
    print len(srv_regs)


def main():

    reg_srvs,srv_regs = registrar_srvs()  # 从数据库中获取所有注册商名称
    save_data(reg_srvs,srv_regs)  # 持久性存储
    reg_srvs, srv_regs = open_data()  # 从文件中读取数据
    count_reg_srv(reg_srvs)   # 统计分析
    count_srv_reg(srv_regs)


if __name__ == '__main__':
    main()




