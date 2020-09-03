# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 10:34:15 2019

@author: 邓磊
"""
import requests
import time
from lxml import etree
import re
import threading

lock = threading.Lock()


class ThreadGetData():
    "多线程抓取数据"

    def __init__(self, urlQueue, conn, cur, sleep=0):
        self.urlQueue = urlQueue
        self.sleep = sleep
        self.conn = conn
        self.cur = cur

        self.init_clean()

    def get_text(self, header):
        "主函数"
        while True:
            try:
                url = self.urlQueue.get(block=False)  # 队列为空 产生异常
            except:
                break
            try:
                req = requests.get(url, headers=header)
            except:
                print(f'无响应，当前网页: {url}')
                time.sleep(60 * 10)
                continue
            print(f'当前抓取网页: {url}')
            url_data = req.text
            if not self.isRight(url_data):
                continue
            # 若网页响应正确, 则分析第一页, 并将总页数填入待爬取队列中
            data = etree.HTML(url_data)
            if url[-6:] == 'page=1':
                self.add_page(data, url)
            # 选取并清洗数据
            Data = self.parse(data)
            self.clean(Data, url)
            time.sleep(self.sleep)

    def parse(self, selector):
        "选取所需数据"
        out = []
        for data in selector.xpath('//div[@class="content"]'):
            # 选取帖子时间, 判断是否存在
            Date = data.xpath(".//p[@class='from']")
            if Date:
                date = Date[0].xpath('.//text()')[1].strip()
            else:
                continue
            # 选取帖子内容
            texts = data.xpath(".//p[@class='txt']")[-1]
            txt = texts.xpath('.//text()')
            txt = ''.join(map(lambda x: x.strip(), txt))
            out.append([date, txt])
        return out

    def clean(self, data, url):
        "清洗并保存数据"
        for date, txt in data:
            # 判断有关键词 ，没有继续执行
            if re.search(self.clc1, txt) or re.findall('#(.*?)#', txt):
                continue
            txt = re.sub(self.clc2, '', txt)
            txt = re.sub(self.clc3, '', txt)
            if len(txt) >= 10:
                lock.acquire(True)
                try:
                    self.cur.execute(
                        f"replace INTO weibo VALUES('{date}', '{txt}')")
                    self.conn.commit()
                except:
                    pass
                lock.release()
        lock.acquire(True)
        self.cur.execute(f"replace INTO url VALUES('{url}', 'yes')")
        self.conn.commit()
        lock.release()

    def add_page(self, data, url):
        "分析总页数, 并加入待爬取队列"
        pages = data.xpath(
            "//a[contains(@href,'page=') and not(@class)]//text()")
        page = len(pages)
        if page <= 1:
            return
        base_url = url.split('=')
        for i in range(2, page + 1):
            base_url[-1] = str(i)
            urls = '='.join(base_url)
            # 判断是否在数据库
            lock.acquire(True)
            value = self.cur.execute(
                f"select 是否抓取 from url where 网址=='{urls}' and 是否抓取=='yes'"
            ).fetchone()
            lock.release()
            if value:  # 在数据库并且已爬取, 则跳过
                continue
            else:  # 不在数据库则写入数据库，并加入队列
                lock.acquire(True)
                self.cur.execute(f"replace INTO url VALUES('{urls}', 'no')")
                self.conn.commit()
                lock.release()
                self.urlQueue.put(urls)

    def isRight(self, url_data):
        "判断网页是否正确响应"
        error = ['您可以尝试更换关键词，再次搜索。']
        for err in error:
            if err in url_data:
                return False
        return True

    def init_clean(self):
        # 创建清洗词语
        error = [
            '展开全文', '网页链接', '发表了', '发布了', '我免费围观了', '分享自',
            '抱歉，由于作者设置，你暂时没有这条微博的查看权限哦。', '抱歉，作者已设置', '该账号因被', '该账号行为异常',
            '我分享了,快来看吧！'
        ]
        clc = '|'.join(error)
        self.clc1 = re.compile(clc)  # 清洗关键词情绪
        self.clc2 = re.compile(
            r'(\s)+|/|更多内容请见长微博。| ​ 收起全文|收起全文|\(.*?\)|【(.*?)】')
        self.clc3 = re.compile('（(.*?)）|『(.*?)』|《(.*?)》|O.*|- 来自.*|d$')
