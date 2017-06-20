# encoding:utf-8
"""
获取域名注册商名称、标准化、持久存储、统计、与标准注册商数量比较、所占域名百分比
标准化方法：
1）lower-case
2）去除名称中的非字母和非数字的字符
3）按照原顺序组成
"""


from fetch_reg_srv_data import update_reg_data
from collections import defaultdict
from collections import Counter
import pandas as pd
import pickle


def open_data():
    """
    打开原始注册商和服务器原始数据文件
    """
    reg_srv_data = pickle.load(open("registrar_srv_data.pkl", "r"))
    return reg_srv_data


def mange_data(reg_srv_data):
    """
    数据处理，去掉注册商名称中的特殊符号，并且与原始名称对应，建立字典
    """
    reg_alias = defaultdict(set)
    original_regs = set()  # 所有注册商名称集合

    for i in reg_srv_data:
        original_reg = i[0].strip()
        original_regs.add(original_reg)
        lower_reg = original_reg.lower()
        filter_reg = filter(str.isalnum, lower_reg)
        reg_alias[filter_reg].add(original_reg)

    return reg_alias, original_regs


def count_reg(reg_alias, original_regs):
    """
    统计各个注册商名称数量分布
    :param reg_alias:
    :return:
    """
    c = Counter()

    for i in reg_alias:
        c[len(reg_alias[i])] += 1

        # 显示特殊情况的注册商
        if len(reg_alias[i]) == 3:
            print i, reg_alias[i]

    print '未处理前共获取注册商数量： ', len(original_regs)
    print '处理后，共获取域名注册商数量： ', len(reg_alias)
    print '名称个数  ', '注册商数量'
    for i in c:
        print i, c[i]


def open_com_reg_raw():
    """
    读取com报告中的注册商和注册商拥有的域名数据
    """
    # 读取com报告中的数据
    reg_df = pd.read_csv('com_registrar_num.csv', names=['reg_name', 'num'])
    return reg_df


def find_same_reg(reg_alias):
    """
    查找相同的域名注册商数量
    :return:
    """
    reg_df = open_com_reg_raw()
    same_reg = []
    total_domain = 0
    for i in reg_df.values:
        reg_name_raw = i[0].strip()
        reg_name_filter = str(filter(str.isalnum, reg_name_raw)).lower()

        if reg_name_filter in reg_alias.keys():
            same_reg.append(reg_name_raw)
            total_domain += i[1]

    print 'com报告中的注册商数量: ', len(reg_df)
    print '探测到的注册商数量: ', len(reg_alias)
    print '共同含有的注册商数量： ', len(same_reg)
    print '所占总共的比例：', len(same_reg)/float(len(reg_df))
    print '共同含有的注册商所负责的域名数量： ',total_domain
    print 'com总共含有的域名数量： ', sum(reg_df['num'])
    print '所占域名比例： ', float(total_domain)/sum(reg_df['num'])

    # 新存在注册商的信息
    for i in set(reg_df['reg_name'])-set(same_reg):
        print i


def alias_query_reg(alias,reg_alias):
    """
    根据简称找到实际名称
    """
    return reg_alias[alias]





def main():
    # update_reg_data(end_tb=8)  # 更新数据
    reg_srv_data = open_data()  # 从文件中读取数据
    reg_alias, original_regs = mange_data(reg_srv_data)
    count_reg(reg_alias, original_regs)   # 统计分析
    find_same_reg(reg_alias)


if __name__ == '__main__':
    main()

