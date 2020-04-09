# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 01:48:20 2020

通过微博高级搜索关键词
网址：https://s.weibo.com/

@author: lei
"""


import pandas as pd
import threading
import re
import time
from queue import Queue
from lxml import etree
import logging
from datetime import datetime, timedelta

from GetUrl import GetUrl
from loginWeibo import Get_cookies


class ThreadGetData(threading.Thread):

    def __init__(self, urlQueue, headers={}):
        # urlQueue - 待爬取网站队列
        # headers  - 表头信息
        super(ThreadGetData, self).__init__()
        self.urlQueue = urlQueue
        self.headers = headers

    def run(self):
        while True:
            try:
                url = self.urlQueue.get(block=False)   # 队列为空 产生异常
            except:
                break
            output = GetUrl(url, headers=self.headers)
            if output.err_url == True:
                err_url.append(output.err_url)

            logging.info('正在解析url:%s' % url)
            selector = etree.HTML(output.data)
            if url[-6:] == 'page=1':    # 如果页码为1,则增加队列
                page = len(selector.xpath(
                    "//a[contains(@href,'page=') and not(@class)]//text()"))
                for i in range(2, page):
                    self.urlQueue.put(url[:-1]+str(i))
            data = selector.xpath("//p[@class='txt']")
            if output.data.find('您可以尝试更换关键词，再次搜索。') != -1:  # 说明爬取有问题，跳转下一网页
                continue

            for t in data:
                txt = t.xpath('.//text()')
                txt = ''.join(map(lambda x: x.strip(), txt))

                # 清洗数据
                if re.search('展开全文|网页链接|发表了|发布了|分享自', txt) == None and re.findall('#(.*?)#', txt) == []:
                    txt = re.sub(
                        r'(\s)+|/|更多内容请见长微博。| ​ 收起全文|收起全文|\(.*?\)|【(.*?)】', '', txt)
                    txt = re.sub(
                        r'（(.*?)）|『(.*?)』|《(.*?)》|O.*|- 来自.*|d$', '', txt)
                    if len(txt) >= 10:
                        result['date'].append(re.findall(
                            r'(\d{4}-\d{2}-\d{2})', url)[0])
                        result['value'].append(txt)
                        result['url'].append(url)
            time.sleep(4)


def getBetweenDay(start, end):
    date_list = []
    begin_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")

    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += timedelta(days=1)
    return date_list


def main(keyword='新冠病毒', start='2020-03-24', end='2020-03-24'):
    # 1.构建爬取队列
    urlQueue = Queue()
    for i in getBetweenDay(start, end):
        url = f'https://s.weibo.com/weibo?q={keyword}&typeall=1&suball=1&timescope=custom:{i}:{i}&Refer=g&page=1'
        urlQueue.put(url)

    # 2.构建表头信息
    cookie = Get_cookies('微博账号', '微博密码')
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2714.400",
              "Cookie": cookie}

    # 3.创建线程
    logging.info('采集线程开始运行--------')
    threadParse = []
    for i in range(4):
        Cthread = ThreadGetData(urlQueue, header)
        time.sleep(3)
        Cthread.start()
        threadParse.append(Cthread)

    # 4.结束线程
    for single in threadParse:
        single.join()
    logging.info("所有采集线程退出循环")

    # 5.保存数据
    df = pd.DataFrame(result)
    df = df.drop_duplicates()
    df.to_excel('爬取结果.xlsx', index=False)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('程序开始运行...')
    start = time.perf_counter()   # 开始计时
    # 定义待爬取数据
    result = {}
    result['date'] = []
    result['value'] = []
    result['url'] = []
    err_url = []

    main()

    end = time.perf_counter()     # 结束计时
    logging.info('程序共运行%.2f秒' % (end-start))
