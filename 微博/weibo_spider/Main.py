# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 00:01:08 2020

@author: Administrator
"""

from Config import keyword, time_start, time_end, clock, UserAgent, cookie, sleep
from func import init_sql, get_time, get_url, main

# 初始化数据库
conn, cur = init_sql()

# 构建待爬取网址时间序列
timescope = get_time(time_start, time_end, clock)

# 构建待爬取网页队列
urlQueue = get_url(timescope, keyword, conn, cur)

# 主程序运行
main(urlQueue, sleep, UserAgent, cookie, conn, cur)
