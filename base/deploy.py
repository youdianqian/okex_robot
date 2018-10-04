#coding=utf-8
# api配置文件
import hashlib
import urllib
try:
    import requests
except:
    pass
import sys
sys.path.append(r'G:\gui_exchange\base\config')
from config.find_config import ReadIni


# api请求的url地址
TRADE_URL = 'https://www.okex.com'
MARKET_URL = 'https://www.okex.com'

# OK的科学上网方式在proxies中设定，小飞机默认本地127.0.0.1：1080端口
def http_get_request(url, params, add_to_headers=None):
    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
    }
    proxies = {
        "http": "http://127.0.0.1:1080",
        "https": "http://127.0.0.1:1080",
    }
    if add_to_headers:
        headers.update(add_to_headers)

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5 ,proxies=proxies)
    except requests.exceptions.ProxyError:
        print("代理链接失败")
        return False
    try:
        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpPost 失败, 详细信息如下:%s,%s" %(response.text,e))
        return


# OK的科学上网方式在proxies中设定，小飞机默认本地127.0.0.1：1080端口
def http_post_request(url, params, add_to_headers=None):
    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
    }
    proxies = {
        "http": "http://127.0.0.1:1080",
        "https": "http://127.0.0.1:1080"
    }
    if add_to_headers:
        headers.update(add_to_headers)
    
    try:
        response = requests.post(url, data=urllib.parse.urlencode(params), headers=headers, timeout=5 ,proxies=proxies)
    except requests.exceptions.ProxyError:
        print("代理链接失败")
        return False
#    print(response)
#    print(response.json())
    try:
        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpPost 失败, 详细信息如下:%s,%s" %(response.text,e))
        return


def api_key_get(params, request_path):
    host_url = TRADE_URL
    params = urllib.parse.urlencode(params)
    url = host_url + request_path 
    response =  http_get_request(url, params)  
    if not response:
        print("psot请求未成功，proxy连接失败")
        return False
    return response


def api_key_post(params, request_path):
    read_ini = ReadIni()
    api_key = read_ini.get_value('api_key')
    secret_key = read_ini.get_value('secret_key')
    params.update({'api_key': api_key})
    host_url = TRADE_URL
    params['sign'] = createSign(params, secret_key)
    url = host_url + request_path 
    response = http_post_request(url, params) 
    if not response:
        print("psot请求未成功，proxy连接失败")
        return False
    return response


# 1. apikey + params + secretkey = sign
# 2. sign + params + apikey  = hexdigest
# secret_key在排序的最末尾
def createSign(Pparams, secret_key):
    read_ini = ReadIni()
    secret_key = read_ini.get_value('secret_key')
    a1 = {}
    a1.update(Pparams)
    sorted_params = sorted(a1.items(), key=lambda x: x[0], reverse=False)
    sorted_params.append(['secret_key',secret_key])
    encode_params = urllib.parse.urlencode(sorted_params)   
    payload = encode_params.encode("utf-8")
    hexdigest = hashlib.md5(payload).hexdigest().upper()
    return hexdigest




