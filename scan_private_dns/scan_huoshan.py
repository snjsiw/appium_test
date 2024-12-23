import hashlib
import sys
import time
import requests
import pprint

if len(sys.argv) < 4:
    print("Usage:")
    print("  python3 ./resolve.py <accountId> <secretKey> <domains> [cip] [type]")
    sys.exit()

accountId=sys.argv[1]
secretKey=sys.argv[2]
domains=sys.argv[3]
cip=sys.argv[4] if len(sys.argv) >= 5 else ""
t=sys.argv[5] if len(sys.argv) == 6 else ""

timeStamp=str(int(1000*(time.time()+3600)))

old=(secretKey, timeStamp, accountId, domains, cip, t)
new=sorted(old)
seperator="_"
newStr=seperator.join(new)
hl = hashlib.md5()
hl.update(newStr.encode(encoding='utf-8'))

qUrl="https://httpdns.volcengineapi.com/resolve?domain=" + domains + "&account_id=" + accountId + "&sign=" + hl.hexdigest() + "&timestamp=" + timeStamp
if len(cip) != 0:
    qUrl = qUrl + "&ip=" + cip
if len(t) != 0:
    qUrl = qUrl + "&type=" + t

print(qUrl)
r = requests.get(qUrl)
if r.status_code == 200:
    pprint.pprint(r.json())
else:
    print(r)

##ID:2102393123
##key:MFNcxdFFy06fAxtB
##在域名管理网站添加*后可以解析全部域名
##域名管理网站：https://console.volcengine.com/TrafficRoute/httpdns/domain
##解析指令：python ./firemoutain.py <ServiceID> <SecretKey> <example.com>

