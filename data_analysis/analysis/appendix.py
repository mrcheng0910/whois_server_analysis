# encoding: utf-8
"""
数据库操作
"""

from db_manage import get_col

col = get_col('com_svr')

domains = col.find({'ips':'216.21.238.34'},{'domain':1,'_id':0})

domain_list = []
for d in domains:
    domain_list.append(d['domain'])

domain_list.sort()

save_file = open('svrCanotWork.txt','w')

for i in domain_list:
    print i
    save_file.write(i+'\n')

print len(domain_list)
save_file.close()
