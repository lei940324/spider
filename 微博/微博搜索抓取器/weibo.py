# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 01:48:20 2020

多线程抓取模板

@author: lei
"""

import numpy as np
import pandas as pd
import threading
import re
import os
import time
from queue import Queue
from lxml import etree
import logging

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
            try : url = self.urlQueue.get(block=False)   # 队列为空 产生异常
            except : break
            output = GetUrl(url, headers=self.headers)
            if output.err_url == True : err_url.append(output.err_url)
            
            logging.debug('正在解析url:%s'%url)
            selector = etree.HTML(output.data)
            text = selector.xpath('//div[@id="articlelistnew"]/div[contains(@class,"articleh")]')
            for t in text:
                result['value'].append(''.join(map(lambda x: x.strip() , t.xpath('./span[1]//text()'))))
            time.sleep(1)
            
            
def main():   
    # 1.构建爬取队列
    urlQueue = Queue()
    for i in range(1,4):
        url='http://guba.eastmoney.com/list,zssh000001,f_{}.html'.format(i)
        urlQueue.put(url)     
    
    # 2.构建表头信息
    cookie = Get_cookies('15806527017', 'z19940324Z.')
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/\
537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 \
Core/1.63.6788.400 QQBrowser/10.3.2714.400"
             "Cookie" : cookie}
    
    # 3.创建线程
    threadParse = []
    for i in range(4):
        Cthread = ThreadGetData(urlQueue, header)
        Cthread.start()
        threadParse.append(Cthread)
    logging.info('采集线程开始运行--------')
    
    # 4.结束线程
    for single in threadParse:
        single.join()
    logging.info("所有采集线程退出循环")
    
    # 5.保存数据
    df = pd.DataFrame(result)
    df.to_excel('爬取结果.xlsx', index = False)
    
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('程序开始运行...')
    start=time.perf_counter()   # 开始计时
    # 定义待爬取数据
    result = {}
    result['value'] = []
    err_url = []
    
    main()
    
    end=time.perf_counter()     # 结束计时
    logging.info('程序共运行%.2f秒'%(end-start))
