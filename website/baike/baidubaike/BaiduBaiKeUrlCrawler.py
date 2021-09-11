# -*- coding: utf-8 -*-
# @Time  : 2021/9/9 2:15
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : BaiduBaikeCrawler.py
import asyncio
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Process

import aiohttp

from website.baike.crawlerBase import CrawlerBaike


class BaiduBaike(CrawlerBaike):
    """收集百度百科并链接存入数据库，并爬取链接中的文本"""
    def __init__(self, redis_url: str):
        super().__init__(redis_url)

    async def crawler_baike_content(self):
        # todo 爬取内容
        pass

    async def get_baike_url_list(self, url: str, session: None):
        html = await self.get_request(url, session)
        url_list = re.findall('((https://baike.baidu.com)?/item/?.*?)"', html)

        url_list = [item[0].replace("\\/", "/").replace("amp;", "") if len(item[1]) != 0
                    else "https://baike.baidu.com%s" % item[0].replace("\\/", "/").replace("\\", "").replace("amp;", "") for item in url_list]
        # 去重
        url_list = set(url_list)
        return url_list

    async def crawler_baike_urls(self):
        async with aiohttp.ClientSession() as session:
            while await self.redis.llen(self.url_queue):
                top_url = await asyncio.wait_for(self.redis.lpop(self.url_queue), 10)
                try:
                    url_list = await self.get_baike_url_list(str(top_url, encoding="utf-8"), session)
                    print(f"已获取{len(url_list)}条链接")
                    for url in url_list:
                        print(f"正在加入{url}")
                        await self.add_url_to_redis(url)
                except aiohttp.client_exceptions.ClientResponseError:
                    continue


if __name__ == '__main__':

    baidu = BaiduBaike("redis://localhost/0")
    baidu.run()





