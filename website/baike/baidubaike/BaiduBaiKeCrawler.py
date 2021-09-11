# -*- coding: utf-8 -*-
# @Time  : 2021/9/11 13:15
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : BaiduBaikeCrawler.py
import asyncio

from website.baike.crawlerBase import CrawlerBaike

"""
百度百科爬虫示例
1. 继承了CrawlerBaike, 并且重写crawler_baike_content方法和run方法
2. 补充爬取逻辑
"""


class BaiduBaiKeCrawler(CrawlerBaike):
    def __init__(self, redis_url: str, task_queue: str):
        """
        :param redis_url: redis的连接url
        :param task_queue: 当前分配到的任务队列的名称
        """
        super().__init__(redis_url)
        self.task_queue = task_queue
        self.submit_queue = task_queue.replace('URL_QUEUE', 'SUBMIT_QUEUE')

    async def submit(self, text: str):
        """
        向队列中提交任务
        :param text: 爬取分好的句子
        :return:
        """
        await self.redis.sadd(self.submit_queue, text)

    async def get_data_from_queue(self):
        """从队列获取一条数据， url链接
        示例：
            url = await self.get_data_from_queue()
            # 转成utf-8
            url = str(url, encoding="utf-8")
        """
        return await self.redis.lpop(self.task_queue)

    async def crawler_baike_content(self):
        """爬取页面数据逻辑
        爬取成功后需要提交数据, 调用
        self.submit(text)
        """
        url = await self.get_data_from_queue()
        # 转成utf-8
        url = str(url, encoding="utf-8")
        print(url)

    def run(self):
        """运行方法
        不用修改
        """
        self.loop.run_until_complete(self.connect())
        self.loop.run_until_complete(
            asyncio.gather(
                *[
                    self.crawler_baike_content()
                ]
            )
        )


if __name__ == '__main__':
    # 固定url
    redis_url = "redis:222.197.201.149/0"
    # 每个人任务不一样
    task = "URL_QUEUE_2"

    baidubaike = BaiduBaiKeCrawler(redis_url, task)
    baidubaike.run()