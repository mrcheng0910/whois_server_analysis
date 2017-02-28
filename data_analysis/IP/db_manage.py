# encoding: utf-8

from pymongo import MongoClient

def get_db():
    """
    连接数据库
    :return
    """
    client = MongoClient('localhost', 27017)
    db = client['whois_sever_analysis']
    return db


def get_col(col_name='ip_scan_result1'):
    """
    获取collection
    :return: col
    """
    db = get_db()
    col = db[col_name]
    return col