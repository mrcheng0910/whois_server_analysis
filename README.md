# whois_server_analysis
对“thin”顶级域名COM的域名WHOIS服务器进行分析，测量其性能和安全性，绘制其在全球的分布。


## 分析的内容

1. IP相关内容  
    * 单个WHOIS服务器的IP数量分布
    * 整体WHOIS服务器的IP数量情况
    * 共用IP的服务器统计
    * IP与注册商的关系
    * IP全球分布
2. 端口相关内容
    * 端口开放统计，长时间进行探测，发现有暂时不提供服务的情况，与ICANN的文件精神不符合。
    * 端口服务之类探测



## 待添加的功能

1. 网络时延抖动
2. ttl，判断操作系统

## 依赖库

项目程序在Ubuntu 14.04 64位系统下运行

1. nmap，安装命令:`apt-get install nmap`
2. libnmap,使用以下命令进行安装
    ```
    $ git clone https://github.com/savon-noir/python-libnmap.git
    $ cd python-libnmap
    $ python setup.py install
    ```
3. 

## 常用数据库命令

1. 分组统计,得到ip的端口状态
```sql
db.getCollection('ip_scan_result').aggregate([{$match:{'state':'up'}},{$group : {_id : "$port_state", num_tutorial : {$sum : 1}}}]);
```