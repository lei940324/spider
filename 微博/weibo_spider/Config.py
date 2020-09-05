# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 19:48:21 2020

@author: 邓磊
"""

# 初始参数设定
keyword = '新冠'  # 关键词
time_start = "2020-01-20"  # 初始时间设定
time_end = "2020-01-20"  # 结束时间设定
clock = [8, 15, 1]  # 分时间搜寻
sleep = 4  # 每抓取一次睡眠时间
respider = True  # 是否重新爬取

cookie = 'SINAGLOBAL=7302312847721.349.1598344126961; UOR=,,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWzpLexbJaLHOf3D4eAUn3N5JpX5KzhUgL.Fo-Ee0eNeoepe0e2dJLoIEXLxKqLBo-LBoMLxK-LBKBLBKMLxKMLB.zL12qLxKMLBK5L1KBLxKBLB.2LB.2t; _s_tentry=login.sina.com.cn; Apache=1359768428468.7239.1599292304516; ULV=1599292304539:7:6:6:1359768428468.7239.1599292304516:1599189215976; WBStorage=70753a84f86f85ff|undefined; WBtopGlobal_register_version=434eed67f50005bd; SCF=Atg0Sh2A3UJ4aztX_fl4S_Ywo10uzKm6TIQi0pvrEQSD8pQFE1GghwAODYkLQGzVslFxfyCs_-mGCvs-W26L4D4.; SUB=_2A25yVzPkDeRhGeNM6FEW8i3NyD-IHXVRJSIsrDV8PUNbmtANLUTTkW9NTj86A2aXxDnEdMGdzZ5oex8-9z8GIAoC; SUHB=0QS5_kVt39mB2j; ALF=1630828340; SSOLoginState=1599292341'
# cookie = loginWeibo('账号', '密码')

UserAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"
