#!/usr/bin/python
# encoding:utf-8
"""
该程序主要用来执行数据库操作，查询以及更新，其他程序调用
@author:程亚楠
@date:2015.3.31
@version1.0
"""
import MySQLdb


class Database:

    def __init__(self, host='172.29.152.176', user='root', passwd='hitnslab', db='domain_whois'):
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

