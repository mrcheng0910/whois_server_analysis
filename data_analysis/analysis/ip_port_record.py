# encoding: utf-8

"""
分析开放IP的43端口的状态和使用服务

@作者：程亚楠
@创建时间：2017.2.28
"""

from collections import Counter
from detected_state_ip import classify_ip_state
from db_manage import get_col


def get_ip_scan_records(ip):
    """
    获取ip的扫描记录
    :param ip: 所要查询的ip，例1.1.2.3
    :return:
        scan_records: 指定IP所有的扫描记录
    """
    col = get_col('ip_scan_result1')
    scan_records = col.find({'ip':ip},{'_id':0,'state':0,'hostname':0,'portid':0})
    return scan_records


def parse_scan_records_state(scan_records, ip):
    """
    解析ip的扫描记录，分析其端口状态（open,closed,filtered）
    :param scan_records: ip的扫描记录
    :param ip: 待分析的ip
    """

    port_state_count = Counter()  # 计数所有记录的端口状态
    record_count = scan_records.count()  # 记录总数

    # 统计各个状态的记录数量
    for r in scan_records:
        port_state_count[r['port_state']] += 1

    open_count = port_state_count['open']/float(record_count)   # open状态所占比
    closed_count = port_state_count['closed']/float(record_count)  # closed状态所占比
    filtered_count = port_state_count['filtered']/float(record_count)   # filtered状态所占比

    print ip, '%.2f%%' % ( open_count* 100),'%.2f%%' % ( closed_count* 100), '%.2f%%' % ( filtered_count* 100)


def manage_scan_records_service(scan_records):
    """
    处理扫描记录的服务情况
    :param scan_records:  扫描记录
    :return:
        port_service_count：端口的服务计数
    """
    port_service_count = Counter()
    for r in scan_records:
        port_service_count[r['port_service']] += 1

    return port_service_count


def ip_port_state(up_ips):
    """
    分析port的状态，主操作
    :param up_ips:
    :return:
    """
    for ip in up_ips:
        scan_records = get_ip_scan_records(ip)
        parse_scan_records_state(scan_records, ip)


def ip_port_service(up_ips):
    """
    分析port的服务，主操作
    :param up_ips:
    :return:
    """
    port_services = []  # 端口所使用的服务
    service_name = set()  # 服务的名字

    #
    for ip in up_ips:
        scan_records = get_ip_scan_records(ip)
        port_service_count = manage_scan_records_service(scan_records)
        service_name = service_name | set(port_service_count.keys())   # 所有服务名字求和
        port_services.append({
            'ip': ip,
            'content': port_service_count
        })
    print 'ip',

    for i in service_name:
        print i,
    print

    for s in port_services:
        print s['ip'],
        total = sum(s['content'].values())
        for i in service_name:
            print '%.2f%%' % (s['content'][i] / float(total) * 100),

        print


if __name__ == '__main__':

    _, up_ips, _ = classify_ip_state()
    ip_port_state(up_ips)
    ip_port_service(up_ips)



