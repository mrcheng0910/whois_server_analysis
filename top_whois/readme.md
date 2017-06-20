从新数据库中获取分析数据。本目录中的脚本，针对服务器、注册商、域名数量进行统计分析，各个代码功能如下介绍：

1. `mysqldb.py`  
数据操作功能
2. `srv_num.py`  
统计服务器地址、数量、对应域名数量、域名总量等，其原始数据保存在`srv_num.pkl`中。
3. `com_registrar_num.csv`  
ICANN发布的官方文件，说明com的域名注册商分布情况
4. `fetch_reg_srv_data.py`  
获取原始注册商和服务器数据，保存在`registrar_srv_data.pkl`文件中
5. `registrar_alias.py`  
统计探测到的域名注册商在com报告中所占比例，以及覆盖域名数量
6. `registrar_svr.py`  
统计探测到的域名注册商和服务器的数量关系



注意： 源数据的更新会影响其他统计数据