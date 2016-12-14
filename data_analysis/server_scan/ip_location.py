# encoding:utf-8
from ip_location.ip2Region import Ip2Region

searcher = Ip2Region('./ip_location/ip2region.db')  # IP定位




def ip2region(ip=None):
    """
    得到IP的地理位置和运营商
    :param ip: 待查询IP
    :return
        city: ip所在城市，若城市为空，则为国家
        network_operator: 运营商，可能为空
    """
    if ip == "" or ip is None:
        return

    data = searcher.btreeSearch(ip)
    print data
    region = data['region']
    region = region.split('|')
    country = region[0]

    return country


print ip2region('8.8.8.8')