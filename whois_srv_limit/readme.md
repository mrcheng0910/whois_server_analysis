目录文件解释如下：

1. `not_found.py`  
对不存在的域名进行WHOIS获取，得到服务器对应的WHOIS记录，发现不存在特征关键字，WHOIS服务器地址从文件`srv_ranking.txt`读取

2. `whois_connect.py`  
与WHOIS服务器进行连接，获取WHOIS信息

3. `socket.py`  
socket交互文件

4. `database.py`  
数据库操作文件

