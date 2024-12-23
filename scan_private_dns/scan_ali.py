import requests
import ipaddress

# 定义需要扫描的网段
nets_to_scan = [
    "203.107.1.0/24",   # 阿里云网段
    "118.184.178.0/24", # 网宿网段
    "119.29.29.0/24"    # 腾讯网段
]

# 定义测试的DNS解析服务地址
test_urls = [
    "http://{}/100000/d?host=www.aliyun.com",
    "http://{}/?ws_domain=www.chinanetcenter.com&ws_cli_IP=1.1.1.1&ws_ret_type=json",
    "https://{}/d?dn=cloud.tencent.com&token=813959707"
]

# 扫描函数，检查每个IP是否有DNS解析响应
def scan_dns_services():
    results = []
    for net in nets_to_scan:
        network = ipaddress.ip_network(net)
        for ip in network.hosts():
            for url_template in test_urls:
                url = url_template.format(ip)
                try:
                    response = requests.get(url, timeout=3)
                    if response.status_code == 200:
                        results.append((str(ip), url, response.text[:100]))  # 限制显示内容
                        print(f"Found DNS Service at {url}")
                except requests.RequestException:
                    pass
    return results

# 执行扫描并打印结果
if __name__ == "__main__":
    scan_results = scan_dns_services()
    for ip, url, content in scan_results:
        print(f"DNS服务发现于IP: {ip}, URL: {url}, 响应内容: {content}")
