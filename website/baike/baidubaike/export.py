# -*- coding: utf-8 -*-
# @Time  : 2021/9/10 21:14
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : export.py
import asyncio
import math

import aioredis
import requests
from aioredis import Redis


async def export(step: int):
    """
    导出爬取的链接数据
    :param step 按照数量来分割
    :return:
    """
    url = "redis://localhost/0"
    redis: Redis = await aioredis.from_url(url)
    urls = await redis.smembers("URL")
    urls = list(urls)
    for i in range(math.ceil(len(urls)/step)):
        with open(f"urls_{i+1}.txt", 'w', encoding='utf-8') as file:
            for url in urls[i*step:min(len(urls), (i + 1) * step)]:
                await redis.rpush(f"URL_QUEUE_{i}", str(url, encoding='utf-8'))
                file.writelines(str(url, encoding='utf-8') + '\n')


if __name__ == '__main__':
    asyncio.run(export(600000))


