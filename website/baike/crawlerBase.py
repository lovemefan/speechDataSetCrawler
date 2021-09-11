# -*- coding: utf-8 -*-
# @Time  : 2021/9/9 1:31
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : crawler.py
import abc
import asyncio

import aiohttp
import aioredis
from aiohttp import ClientResponse
from aioredis import Redis


class CrawlerBaike:
    """百科爬虫父类，
     1. 规定crawler_baike_urls为爬取链接
     2. 规定crawler_baike_content根据uri为爬取内容
     继承该类需要重写：
        * crawler_baike_urls() # 爬取urls链接存入reids的业务逻辑

        * crawler_baike_content(uri: str) #根据某个uri 爬取 网站内容的业务逻辑

        * run() # 总业务逻辑
     """

    def __init__(self, redis_url: str):
        self.redis = None
        self.url = redis_url
        self.loop = asyncio.get_event_loop()
        self.url_set = "URL"
        self.url_queue = "URL_QUEUE"

    async def connect(self):
        """
        建立与reids的连接
        :return:
        """
        if self.redis is None:
            self.redis: Redis = await aioredis.from_url(self.url)

    async def get_request(self, url: str, session: None) -> ClientResponse:
        """
        get 网络请求
        :param session:
        :param url: 网路url
        :return:  网络response
        """
        if session is None:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.text()
        else:
            async with session.get(url) as response:
                return await response.text()


    @abc.abstractmethod
    async def crawler_baike_content(self):
        """
        根据分发到的百科uri任务， 将文本爬取下来
        :return:
        """
        pass

    @abc.abstractmethod
    async def crawler_baike_urls(self):
        """
        爬取 百科将url存入redis的set中保证不重复
        :return:
        """
        # 插入测试
        await self.add_url_to_redis("sina.com")

    async def add_url_to_redis(self, url: str):
        """
        将url添加到redis中去重,
        redis 中会维护一个名为`URL`的集合 和一个为 `URL_QUEUE` 的list队列
        :param url:
        :return:
        """
        # 如果当前uri不在集合中着插入队列和集合中
        if await self.redis.sismember(self.url_set, url) == 0:
            await self.redis.rpush(self.url_queue, url)
            await self.redis.sadd(self.url_set, url)

    def run(self):
        self.loop.run_until_complete(self.connect())
        self.loop.run_until_complete(
            asyncio.gather(
                *[
                    self.crawler_baike_urls(),
                    self.crawler_baike_content()
                ]
                )
        )




if __name__ == '__main__':
    # 测试
    crawler = CrawlerBaike("redis://localhost/0")
    crawler.run()

