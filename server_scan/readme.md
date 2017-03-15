## 功能介绍

1. 系统数据库使用Mongodb
2. 数据库服务器地址：152服务器上
3. 数据库名称whois_server_analysis


## 文件功能介绍

* db_manage.py   
    数据库操作文件
* insert_source_svr.py  
    将文件中的WHOIS服务器地址存入到Mongodb数据库中,collection名称com_svr.
* net_state.py  
    网络延迟探测
* reverse_ip.py  
    探测whois服务器域名的ip地址列表，并更新数据库
* server_probe.py   
    对ip的43端口进行tcp扫描
* com_svr.txt   
    com的二级WHOIS服务器地址
    

## 特殊情况记录

1. whois.no-ip.com  
需要间隔2秒进行查询。
