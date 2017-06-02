# encoding:utf-8
"""
获取域名注册商名称、标准化、持久存储、统计、与标准注册商数量比较、所占域名百分比
标准化方法：
1）lower-case
2）去除名称中的非字母和非数字的字符
3）按照原顺序组成
"""


from mysqldb import MySQL
from collections import defaultdict
from collections import Counter
import pandas as pd
import pickle


def registrar_alias():
    """
    统计域名注册商的别名，即在WHOIS信息中，域名注册商的名字出现多少种样式
    包括大小写、名称中间有标点、名称后有标点
    :return:
    """
    mysql = MySQL(HOST='172.29.152.249', USER='root', PASSWORD='platform')
    mysql.connect()
    mysql.select_db('domain_whois')

    reg_alias = defaultdict(set)  # 存储转换后的注册商和原始注册商名称

    for table_num in xrange(1, 101):
        print 'table: ', str(table_num)
        sql = """SELECT DISTINCT(sponsoring_registrar) FROM domain_whois_{n} \
              WHERE tld = 'com' AND sponsoring_registrar != ''""".format(n=table_num)

        registrar_data = mysql.execute_sql(sql)[0]

        for i in registrar_data:
            original_reg = i[0].strip()
            lower_reg = original_reg.lower()
            filter_reg = filter(str.isalnum, lower_reg)
            reg_alias[filter_reg].add(original_reg)

    mysql.disconnect()

    return reg_alias

def save_data(reg_alias):

    # 将 obj 持久化保存到文件 reg_alias.txt 中
    pickle.dump(reg_alias, open("reg_alias.txt", "w"))


def open_data():
    # 从 reg_alias.txt 中读取并恢复 obj 对象
    reg_alias = pickle.load(open("reg_alias.txt", "r"))
    return reg_alias


def count_reg(reg_alias):
    """
    统计各个注册商名称数量分布
    :param reg_alias:
    :return:
    """
    c = Counter()
    print '总共注册商数量: ',len(reg_alias)

    for i in reg_alias:
        for j in reg_alias[i]:
            print j
        c[len(reg_alias[i])] += 1
        # if len(reg_alias[i]) == 1:
        #     print i, reg_alias[i]
            # for j in reg_alias[i]:
            #     print j

    print '不同名称个数的注册商数量分布：'
    print '名称个数  ','注册商数量'
    # for i in c:
    #     print i, c[i]


def open_com_reg_raw():
    """
    读取com报告中的注册商和注册商拥有的域名数据
    """
    # 读取com报告中的数据
    reg_df = pd.read_csv('com_registrar_num.csv', names=['reg_name', 'num'])
    return reg_df


def find_same_reg(reg_df, reg_alias):
    """
    查找相同的域名注册商数量
    :return:
    """
    same_reg = []
    total_domain = 0
    for i in reg_df.values:
        reg_name_raw = i[0].strip()
        reg_name_filter = filter(str.isalnum, reg_name_raw).lower()

        if reg_name_filter in reg_alias.keys():
            same_reg.append(reg_name_raw)
            total_domain += i[1]

    print 'com报告中的注册商数量: ', len(reg_df)
    print '共同含有的注册商数量： ', len(same_reg)
    print '所占总共的比例：', len(same_reg)/float(len(reg_df))
    print '共同含有的注册商所负责的域名数量： ',total_domain
    print 'com总共含有的域名数量： ',sum(reg_df['num'])
    print '所占域名比例： ', float(total_domain)/sum(reg_df['num'])

    # 新存在注册商的信息
    # for i in set(reg_df['reg_name'])-set(same_reg):
    #     print i


def main():

    # reg_alias = registrar_alias()  # 从数据库中获取所有注册商名称
    # save_data(reg_alias)  # 持久性存储
    reg_alias = open_data()  # 从文件中读取数据
    count_reg(reg_alias)   # 统计分析
    df = open_com_reg_raw()
    find_same_reg(df,reg_alias)


if __name__ == '__main__':
    main()




