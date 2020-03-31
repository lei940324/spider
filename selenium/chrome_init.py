# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 20:19:17 2020

对谷歌浏览器初始化设置

@author: lei
"""

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def chrome(show=True, picture=False):
    opt = Options()
    opt.add_argument('--no-sandbox')
    opt._arguments = ['disable-infobars']
    opt.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
    opt.add_argument('--disable-gpu')
    opt.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    if not picture:
        opt.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # 加载用户信息的谷歌浏览器
    opt.add_argument(
        "--user-data-dir="+r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data")
    if not show:
        # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        opt.add_argument('--headless')
    # 以最高权限运行
    opt.add_argument('--no-sandbox')
    # 禁用浏览器弹窗
# =============================================================================
#     prefs = {
#     'profile.default_content_setting_values' :  {
#         'notifications' : 2
#          }
#     }
#     opt.add_experimental_option('prefs',prefs)
# =============================================================================

    # 禁用弹出拦截
    # opt.add_argument('--disable-popup-blocking')
    # 禁用JavaScript
    # opt.add_argument("--disable-javascript")
    # 修改UA
    #opt.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
    driver = webdriver.Chrome(chrome_options=opt)  # 调用带参数的谷歌浏览器
    driver.maximize_window()  # 窗口最大化
    wait = WebDriverWait(driver, 15)
    return driver, wait


if __name__ == '__main__':
    url = 'https://daohang.qq.com/?fr=hmpage'
    driver, wait = chrome()
    driver.get(url)
