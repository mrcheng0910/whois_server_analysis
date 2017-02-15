# encoding: utf-8

"""
将文件中的WHOIS服务器存入到Mongodb数据库中，默认服务器的ip为空
作者：程亚楠
时间：2017.2.15
"""

from db_manage import get_db
from datetime import datetime


def insert_svr(col_name,source_file_name):
    """
    将待查询的whois服务器插入到数据库中
    col_name: 数据库collection名称
    source_file_name: 服务器源文件名称
    """

    db = get_db()
    col = db[col_name]
    svr_file = open(source_file_name,'r')  # 打开文件
    for svr in svr_file.readlines():
        svr_name = svr.strip()

        # 若数据库中不存在该服务器地址则插入
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
    print '操作完成'


if __name__ == '__main__':

    col_name = 'com_svr'
    svr_file_name = 'com_svr.txt'
    insert_svr(col_name,svr_file_name)