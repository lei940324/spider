# -*- coding: utf-8 -*-
"""
Created on Sat May 25 15:38:06 2019

使用selenium抓取数据模板

@author: lei
"""

import time
import re
import requests
import numpy as np
import pandas as pd
from selenium.webdriver.common.by import By
from selenium_chrome import chrome
from selenium.webdriver.support import expected_conditions as EC


class Spyder():
    # file_name为保存文件名
    def __init__(self, file_name='数据结果.xlsx'):
        self.file_name = file_name
        self.driver, self.wait = chrome()
        self.run()

    def run(self):
        self.defined_var()     # 第一步：定义待爬取数据
        self.generate_urls()   # 第二步：生成待爬取网址
        self.main()            # 第三步：爬取主要过程
        self.driver.close()    # 第四步：关闭谷歌浏览器
        self.clean_data()      # 第五步：清洗数据
        self.save_data()       # 第六步：保存数据

    def defined_var(self):  # 定义待爬取数据
        self.value = []  # 原始数据
        self.val = []   # 清洗后数据

    def generate_urls(self):
        pass

    def main(self):
        pass

    def clean_data(self):   # 清洗数据
        pass

    def save_data(self):
        df = pd.DataFrame(self.val, columns=['爬取结果'])
        df.to_excel(self.file_name, index=False)
# =============================================================================
# with open(self.file_name,'w',encoding='utf-8') as f:
#         for i in val:
#             f.write('{}\n'.format(i))
# =============================================================================


if __name__ == '__main__':
    example = Spyder()
