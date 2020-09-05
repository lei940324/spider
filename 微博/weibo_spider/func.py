# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 20:53:41 2020

@author: Administrator
"""
import datetime
import threading
import sqlite3
import time
from urllib.parse import urlencode
from queue import Queue

from ThreadGetData import ThreadGetData


def init_sql():
    "初始化数据库"
    # 创建与数据库的连接
    conn = sqlite3.connect('data.db', check_same_thread=False)
    cur = conn.cursor()
    # 判断 weibo 与 url 两表是否存在，不存在则创建
    weibo = cur.execute(
        "select count(*) from sqlite_master where type='table' and name = 'weibo';"
    ).fetchall()
    if weibo[0][0] == 0:
        sql_text = '''CREATE TABLE weibo
            (时间 TEXT,
                内容 TEXT PRIMARY KEY); '''
        cur.execute(sql_text)

    url = cur.execute(
        "select count(*) from sqlite_master where type='table' and name = 'url';"
    ).fetchall()
    if url[0][0] == 0:
        sql_text = '''CREATE TABLE url
            (网址 TEXT PRIMARY KEY,
                是否抓取 TEXT); '''
        cur.execute(sql_text)
    return conn, cur


def get_time(time_start, time_end, clock):
    "构建待爬取网址时间序列"
    d1 = datetime.timedelta(days=1)
    start = datetime.datetime.strptime(time_start, '%Y-%m-%d')
    end = datetime.datetime.strptime(time_end, '%Y-%m-%d')
    day = (end - start).days
    date = [
        datetime.datetime.strftime(start + i * d1, '%Y-%m-%d')
        for i in range(day + 1)
    ]

    if clock:  # 分时搜索
        time_date = []
        for value in date:
            i, j, k = clock
            series = [i for i in range(i, j, k)]
            for h in series:
                time_date.append(f'{value}-{h}:{value}-{h+1}')
        return time_date
    else:
        return [f'{i}:{i}' for i in date]


def get_url(timescope, keyword, respider, conn, cur):
    "构建待爬取网页队列"
    urlQueue = Queue()
    base_url = 'https://s.weibo.com/weibo?'

    for value in timescope:
        params = {
            'q': keyword,
            'typeall': 1,
            'suball': 1,
            'timescope': 'custom:' + value,
            'Refer': 'g',
            'page': 1
        }
        url = base_url + urlencode(params)
        # 判断 page=1 是否在数据库
        value = cur.execute(
            f"select 是否抓取 from url where 网址=='{url}' and 是否抓取=='yes'"
        ).fetchone()
        if value and not respider:  # 在数据库并且已爬取，则跳过
            continue
        else:  # 不在数据库，则将网址放入数据库
            cur.execute(f"replace INTO url VALUES('{url}', 'no')")
            conn.commit()
    # 将数据库中所有未爬取网址放入队列
    urls = cur.execute(f"select 网址 from url where 是否抓取=='no'").fetchall()
    for url in urls:
        urlQueue.put(url[0])
    return urlQueue


def main(urlQueue, sleep, UserAgent, cookie, respider, conn, cur):
    header = {"User-Agent": UserAgent, 'Cookie': cookie}
    # 记录线程的列表
    threadCrawl = []
    print('4个采集线程开始运行--------')
    for _ in range(4):
        Cthread = ThreadGetData(urlQueue, respider, conn, cur, sleep)
        threadObj = threading.Thread(target=Cthread.get_text, args=[header])
        threadObj.start()
        threadCrawl.append(threadObj)
        time.sleep(2)

    # 等待所有待爬取网页全部响应，也就是等待之前的操作执行完毕,采集线程退出循环
    for single in threadCrawl:
        single.join()
    print("所有采集线程退出循环")

    cur.close()  # 关闭游标
    conn.close()  # 关闭连接
