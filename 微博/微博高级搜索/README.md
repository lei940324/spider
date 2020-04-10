<a href="https://www.python.org/downloads/"><img  src="https://img.shields.io/badge/python-3.6%2B-brightgreen"></a>
<a href="https://github.com/psf/requests"><img src="https://img.shields.io/badge/requests-2.22.0-yellow"></a>
<a href="https://github.com/pandas-dev/pandas"><img src="https://img.shields.io/badge/pandas-1.0.1-yellow"></a>
<a href="https://github.com/lxml/lxml"><img src="https://img.shields.io/badge/lxml-4.5.0-red"></a>

# 介绍

通过微博高级搜索功能，使用关键词进行信息检索，可以通过设定时间抓取

网址：https://s.weibo.com/

![image-20200409221623118](https://raw.githubusercontent.com/lei940324/picture/master/typora202004/09/221936-923226.png)


# 使用

```python
设定代码main函数中参数：
keyword -  搜索关键词
start   -  开始日期
end     -  结束日期
cookie = Get_cookies('微博账号', '微博密码')   
```

最后命令行输入：

```python
python weibo.py
```

