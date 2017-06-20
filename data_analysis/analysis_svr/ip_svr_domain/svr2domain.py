# encoding: utf-8
"""
根据二级服务器名称，获取域名，并将域名保存文件
"""

from data_analysis.analysis_svr.ip_svr_domain.db_mysql import Database


def get_svr():

    ip_svr = []
    svr_file = open('ip_svr','r')
    for i in svr_file:
        ip_svr.append(i.strip())

    return ip_svr


def get_domain():

    db = Database()
    ip_svr = get_svr()

    for i in ip_svr:
        sql = 'SELECT domain FROM domain_whois_1 WHERE sec_whois_server = "%s" LIMIT 20' % i.split(' ')[1]
        print sql

        domains = db.select_domain(sql)

        file_name = i.replace(' ','-')+'.txt'
        domain_file = open('./domain/'+file_name,'w')

        for i in domains:
            print i[0]
            domain_file.write(i[0]+'\n')

        domain_file.close()

    db.close_db()

get_domain()