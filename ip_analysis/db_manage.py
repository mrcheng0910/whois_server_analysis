# encoding: utf-8
"""
数据库操作
"""

from pymongo import MongoClient

server_address = 'localhost'
client_name = 'whois_server_analysis'

def get_db():
    """
    连接数据库
    :return
    """
    client = MongoClient(server_address, 27017)
    db = client[client_name]
    return db


def get_col(col_name='ip_scan_result1'):
    """
    获取collection
    :return: col
    """
    db = get_db()
    col = db[col_name]
    return col
