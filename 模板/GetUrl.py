# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 22:51:32 2020

单线程抓取模板

@author: lei
"""

import time
import requests
import logging


class GetUrl():
    def __init__(self, url, num=5, headers={}, level=3):
        # url     - 待爬取网站
        # num     - 网站响应失败后,最大爬取次数
        # headers - 表头信息
        # level   - 信息显示等级,0级最低,5级最大
        # err_url - 抓取失败的网站汇总
        # data    - 爬取数据
        self.url = url
        self.num = num
        self.headers = headers
        self.level = level
        self.err_url = ''
        self.data = ''
        self.run()

    def run(self):
        self.Info_level()
        self.data = self.judge()

    def Info_level(self):
        levels = [logging.NOTSET, logging.DEBUG, logging.INFO,
                  logging.WARNING, logging.ERROR, logging.CRITICAL]
        logging.basicConfig(level=levels[self.level])

    def response(self):
        try:
            req = requests.get(self.url, headers=self.headers, timeout=30)
            req.raise_for_status()
            req.encoding = 'utf-8'
            logging.debug('Python 返回URUL:%s  数据成功' % self.url)
            return req.text
        except:
            logging.debug('Python 返回URL:%s  数据失败' % self.url)
            return ''

    def judge(self):
        n = 1
        while n <= self.num:
            logging.debug(f'开始第{n}次加载.......')
            data = self.response()
            if data:
                break
            n += 1
            time.sleep(2)
        if data == '':
            logging.debug('***************************************')
            logging.debug('爬取次数已达到最大限制,已跳过URL:%s' % self.url)
            logging.debug('***************************************')
            self.err_url = self.url
        return data


if __name__ == '__main__':
    cookie = ''
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2714.400",
              'Cookie': cookie}
    url = 'https://www.baidu.com/'

    data = GetUrl(url, headers=header).data
