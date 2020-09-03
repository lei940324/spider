# -*- encoding:utf-8 -*-

import base64
import requests
import re
import rsa
import binascii


def Get_cookies(username, password):
    '''登陆新浪微博，获取登陆后的Cookie，返回到变量cookies中'''

    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.4)%' + \
        username
    html = requests.get(url).content.decode('utf-8')

    servertime = re.findall('"servertime":(.*?),', html, re.S)[0]
    nonce = re.findall('"nonce":"(.*?)"', html, re.S)[0]
    pubkey = re.findall('"pubkey":"(.*?)"', html, re.S)[0]
    rsakv = re.findall('"rsakv":"(.*?)"', html, re.S)[0]

    username = base64.b64encode(username.encode())  # 加密用户名
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
    message = str(servertime) + '\t' + str(nonce) + \
        '\n' + str(password)  # 拼接明文js加密文件中得到
    passwd = rsa.encrypt(message.encode('utf-8'), key)  # 加密
    passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。

    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.4)'
    data = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'ssosimplelogin': '1',
        'vsnf': '1',
        'vsnval': '',
        'su': username,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'sp': passwd,
        'encoding': 'UTF-8',
        'prelt': '115',
        'rsakv': rsakv,
        'url':
        'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    html = requests.post(login_url, data=data).content.decode('gbk')
    urlnew = re.findall('location.replace\(\'(.*?)\'', html, re.S)[0]

    # 发送get请求并保存cookies
    cookies = requests.get(urlnew).cookies.items()

    cookie = ''
    for name, value in cookies:
        cookie += '{0}={1};'.format(name, value)

    return cookie


if __name__ == '__main__':
    cookie = Get_cookies('账号', '密码')
    header = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400",
        'Cookie': cookie
    }
    url = 'https://s.weibo.com/weibo?q=中美贸易战&Refer=index'
    data = requests.get(url, headers=header).text
