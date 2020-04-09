# 介绍

通过微博高级搜索功能，使用关键词进行信息检索，可以通过设定时间抓取

网址：https://s.weibo.com/

![image-20200409221623118](https://raw.githubusercontent.com/lei940324/picture/master/typora202004/09/221936-923226.png)

# 要求

* python3.6+
* 第三方库：`requests`、`pandas`、`lxml`

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

