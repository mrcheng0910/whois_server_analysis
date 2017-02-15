# encoding: utf-8

"""
将文件中的WHOIS服务器存入到Mongodb数据库中，默认服务器的ip为空
"""

from db_manage import get_db
from datetime import datetime


def insert_svr(col_name,source_file_name):
    """
    将待查询的whois服务器插入到数据库中
    :return:
    """
    db = get_db()
    col = db[col_name]
    svr_file = open(source_file_name,'r')  # 打开文件
    for svr in svr_file.readlines():
        svr_name = svr.strip()
        print svr_name

        # 若数据库不存在该服务器则插入
        col.update(
            {'domain':svr_name},
            {
                '$setOnInsert':
                {
                    'domain':svr_name,
                    'ips':[],
                    'inserted_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
             },
            True
        )

    svr_file.close()  # 关闭文件


if __name__ == '__main__':

    col_name = 'com_svr'
    svr_file_name = 'com_svr.txt'
    insert_svr(col_name,svr_file_name)