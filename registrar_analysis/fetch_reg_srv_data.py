# encoding:utf-8
"""
域名注册商所含有的域名服务器分布
"""

from mysqldb import MySQL
import pickle


def registrar_srvs(end_tb):
    """
    获取原始数据
    """
    mysql = MySQL(HOST='172.29.152.249', USER='root', PASSWORD='platform')
    mysql.connect()
    mysql.select_db('domain_whois')
    registrar_srv_data = None
    for table_num in xrange(1, end_tb):
        print 'table: ', str(table_num)
        sql = """SELECT sponsoring_registrar, sec_whois_server FROM domain_whois_{n} WHERE tld='com' AND sponsoring_registrar!='' AND sec_whois_server!='' GROUP BY sponsoring_registrar,sec_whois_server""".format(n=table_num)
        registrar_srv_data = mysql.execute_sql(sql)[0]

    mysql.disconnect()

    return registrar_srv_data


def save_data(registrar_srv_data):
    pickle.dump(registrar_srv_data, open("registrar_srv_data.pkl", "w"))


def update_reg_data(end_tb=2):
    """
    :param end_tb: 最终表名称
    :return:
    """
    registrar_srv_data = registrar_srvs(end_tb)  # 从数据库中获取所有注册商名称
    save_data(registrar_srv_data)  # 持久性存储


if __name__ == '__main__':
    update_reg_data()




