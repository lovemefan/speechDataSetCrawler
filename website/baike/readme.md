# 百度百科，维基百科爬虫

## 文件目录

```
│  crawlerBase.py
│  readme.md
└──baidubaike
      BaiduBaikeCrawler.py

```
## 使用
1. 启动redis后在代码中配置
2. 加入一个任意的起始的百度百科链接

    redis 运行命令
    ```bash
    SADD URL https://baike.baidu.com/item/%E7%99%BD%E5%9E%A9%E7%BA%AA%E5%9B%BD%E5%AE%B6%E5%9C%B0%E8%B4%A8%E5%85%AC%E5%9B%AD/18414471
    LPUSH URL_QUEUE https://baike.baidu.com/item/%E7%99%BD%E5%9E%A9%E7%BA%AA%E5%9B%BD%E5%AE%B6%E5%9C%B0%E8%B4%A8%E5%85%AC%E5%9B%AD/18414471
    ```
3. 运行
    ```bash
    python BaiduBaikeCrawler.py
    ```