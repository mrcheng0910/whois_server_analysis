#!/usr/bin/python
# encoding:utf-8
"""
该程序主要用来执行数据库操作，查询以及更新，其他程序调用
@author:程亚楠
@date:2015.3.31
@version1.0
"""
import MySQLdb



host = '42.236.61.59'
user='root'
passwd='cncert0728+@+::'
db='malicious_url_whois'

class Database:

    def __init__(self, host='172.29.152.249', user='root', passwd='platform', db='malicious_url_whois'):
        """
        数据库初始化
        """
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = 'utf8'

    def __get_connect(self):
        """
        执行连接数据库操作
        """
        if not self.db:
            raise(NameError, 'There is not db information')
        try:
            self.conn = MySQLdb.Connection(
                host=self.host, user=self.user, passwd=self.passwd, db=self.db, charset=self.charset)
        except:
            raise(NameError, 'Connect failure')
        cursor = self.conn.cursor()
        if not cursor:
            raise(NameError, "Connect failure")
        else:
            return cursor

    def close_db(self):

        self.conn.commit()
        self.conn.close()

    def select_domain(self,sql=''):

        if sql:
            cursor = self.__get_connect()
            cursor.execute(sql)
            return cursor.fetchall()
        else:
            return



# db = Database(host=host,user=user,passwd=passwd,db=db)
db = Database()

sql = 'select updated_date,domain from whois WHERE updated_date != "" '
# sql = 'select creation_date,domain from whowas WHERE creation_date != "" '

domains = db.select_domain(sql)
print len(domains)
import datetime

c = datetime.datetime.now()
error_count = 0

for i in domains:
    # ud = i[0].split('T')[0].split(' ')[0]
    try:
        y = datetime.datetime.strptime(i[0], '%Y-%m-%d')
        print y
        during_day = (c-y).days
        if during_day <= 90:
            print during_day
            print i[1]
    except:
        error_count += 1
        pass

print error_count
