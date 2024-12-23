import hashlib
import time
import requests

def generate_signature(dn, key, t):
    """生成鉴权字符串"""
    sign_str = f"{dn}-{key}-{t}"
    return hashlib.md5(sign_str.encode()).hexdigest()

def httpdns_request(service_address, account_id, dn, qt='A', ip='1.1.1.1', key='f89dbd2b722ab0fa2a4bd888c33cba4a'):
    """发送HTTP DNS请求"""
    # 获取当前时间戳
    t = str(int(time.time()))
    # 生成鉴权字符串
    s = generate_signature(dn, key, t)

    # 构建请求URL
    url = f"http://{service_address}/v1/{account_id}/d"

    # 请求参数
    params = {
        'dn': dn,
        'qt': qt,
        'ip': ip,
        't': t,
        's': s
    }

    # 发送GET请求
    response = requests.get(url, params=params)

    # 检查响应状态码
    if response.status_code == 200:
        # 请求成功，打印解析结果
        return response.json()
    else:
        # 请求失败，打印错误信息
        return {'error': 'Request failed', 'status_code': response.status_code, 'response': response.text}


# 使用示例
service_address = '116.198.3.251'  # 服务地址
account_id = '108086391060888821'  # 账户ID
dn = 'baidu.com'  # 待解析的域名
key = 'f89dbd2b722ab0fa2a4bd888c33cba4a'  # 用户密钥

# 发起请求
result = httpdns_request(service_address, account_id, dn, key=key)

# 打印结果
print(result)