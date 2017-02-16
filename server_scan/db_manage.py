# encoding:utf-8
"""
database functions
"""

from pymongo import MongoClient


def get_db():
    """
    获取数据库
    :return
    其他：可以完善
    """
    client = MongoClient('localhost', 27017)
    db = client['whois_sever_analysis']
    return db







def get_open_ip():
    """
    Get the open ips
    :return:
    """
    db = get_db()
    col = db['scan_info']
    ips = col.find({'state':'up'},{'_id':0,'ip':1}).distinct('ip')
    print len(ips)
    return ips


def insert_net_state(net_state):
    """
    Insert the net state of ip into database
    :param net_state:
    :return:
    """
    db = get_db()
    col = db['ip_net_state']
    print col.insert_one(net_state)



