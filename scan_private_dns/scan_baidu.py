import hashlib
import time
import requests
import json


def generate_signature(dn, secret, timestamp):
    """生成鉴权签名"""
    sign_str = f"{dn}-{secret}-{timestamp}"
    return hashlib.md5(sign_str.encode()).hexdigest()


def httpdns_request(account_id, dn, secret):
    """发送HTTP DNS请求"""
    # 获取当前时间戳
    timestamp = str(int(time.time()))
    # 生成鉴权签名
    sign = generate_signature(dn, secret, timestamp)

    # 构建请求URL
    url = f"http://180.76.76.200/v3/resolve"

    # 请求参数
    params = {
        'account_id': account_id,
        'dn': dn,
        'sign': sign,
        't': timestamp,
    }

    # 发送GET请求
    response = requests.get(url, params=params)

    # 检查响应状态码
    if response.status_code == 200:
        # 请求成功，解析JSON响应
        return response.json()
    else:
        # 请求失败，抛出异常
        response.raise_for_status()


# 使用示例
account_id = '115115'  # 您的账户ID
dn = 'baidu.com'  # 待解析的域名
secret = 'sE4g9X8THsNuW1YSstiC'  # 您的密钥

try:
    result = httpdns_request(account_id, dn, secret)
    print(json.dumps(result, indent=4, ensure_ascii=False))
except requests.exceptions.RequestException as e:
    print(f"请求失败：{e}")