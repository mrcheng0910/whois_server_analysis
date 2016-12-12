# encoding:utf-8
"""
数据库操作
"""

import json
from collections import Counter
from collections import defaultdict
from pymongo import MongoClient
from datetime import datetime

def get_db():
    """
    获取数据库
    :return
    其他：可以完善
    """
    client = MongoClient('localhost', 27017)
    db = client['whois_sever_analysis']
    return db


def insert_svr():
    """
    将待查询的whois服务器插入到数据库中
    :return:
    """
    db = get_db()
    col = db['svr_source']
    svrs = open('test.txt','r')
    for svr in svrs.readlines():
        svr_level = svr.strip().split('\t')
        if len(svr_level) != 2 or svr_level[1]=='':
            pass
        else:
            # 若数据库不存在该服务器则插入
            col.update(
                {'domain':svr_level[0]},
                {'$setOnInsert':{'domain':svr_level[0],'level':svr_level[1],'ips':[]}},
                True
            )

    svrs.close()

# insert_svr()









