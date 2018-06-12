# 网易云音乐评论爬虫
### 运行环境：

> Mysql >= 5.6、Python3

### 功能

> 输入某个昵称，爬取该昵称的歌单中歌曲的评论(目前支持爬取前100个歌单)，包括自建、收藏歌单

### 使用

首先需要配置在`settings.py`配置好数据库连接如下

```shell
#database config
MYSQL_HOST = "127.0.0.1"
MYSQL_DBNAME = "scrapy"
MYSQL_USER = "root"
MYSQL_PASSWORD = "toor"
MYSQL_PORT = 3306
```

因为爬虫长时间爬取会被禁IP，支持设置代理池，为空则不使用代理，不需要某个特定代理API，调用的API只要每次请求能返回一个有效代理即可

```shell
#proxy api url, get a proxy from the url
# http://dynamic.goubanjia.com/dynamic/get/01aa529ed9315a3ca9488766736cdd40.html?sep=3
PROXY_API_URL = ''
```

### 使用方法

> scrapy crawl music_163_comments -a nickname=yournickname 

开始爬取后会将评论自动插入到`scrapy`数据库的`music_163_com_comments`表中

### 备注

1. 使用了2018.5可用的API实现，不保证以后能正常使用
2. 如果不使用代理池的话大概爬取将近100W评论将会被BAN,过几个小时恢复正常
3. 第一次写爬虫，存在些小问题，不影响整体使用，日后有需要再修复