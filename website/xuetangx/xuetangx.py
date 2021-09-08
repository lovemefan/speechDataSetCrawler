# -*- coding: utf-8 -*-
# @Time  : 2021/3/16 19:47
# @Author : lovemefan
# @File : xuetanzaixian.py
import asyncio
import sys
import os
sys.path.append(os.getcwd())
# import gevent
# from gevent import monkey
# monkey.patch_all()
from moviepy.video.io.VideoFileClip import VideoFileClip

sys.path.append(os.path.dirname(os.path.abspath(os.pardir)))
print(os.path.dirname(os.path.abspath(os.pardir)))
import re

import requests
from tqdm import tqdm

from config.Config import Config
from utils.MediaDownloader import MediaDownloader
import json
from bs4 import BeautifulSoup

from utils.log import logger

class xuetangx(MediaDownloader):

    def __init__(self, *base_dirs):
        self.headers = {
                            "cookie": "provider=xuetang; django_language=zh; _ga=GA1.2.1070881427.1615894932; _gid=GA1.2.1120574251.1615894932; login_type=WX; csrftoken=Suf7suanEuttxHfINy6btjNdMvWHcjwJ; sessionid=hk2htylts3wrgb7dsesqd6gdpw8rq5f8; k=32717444; _gat_gtag_UA_164784773_1=1",
                            "xtbz": "xt"
                        }
        self.save_path = Config.get_instance().get('file.save_path')
        self.course_name = ''

    def join_course(self, cid, sign):
        base_url = f"https://www.xuetangx.com/api/v1/lms/product/sku_pay_detail/?cid={cid}&sign={sign}"
        result = json.loads(requests.get(base_url).text)
        product_id = result['data']['product_id']
        sku_id = result['data']['sku_info'][0]['sku_id']
        url = f"https://www.xuetangx.com/api/v1/lms/order/entries_free_sku/{product_id}/?sid={sku_id}"
        result = json.loads(requests.get(url, headers=self.headers).text)
        print(f"加入课堂{'成功' if result['success'] else '失败, 可能已经加入了'}")

    def get_course_list(self, cid, sign):
        base_url = f"https://www.xuetangx.com/api/v1/lms/learn/course/chapter?cid={cid}&sign={sign}"
        response = json.loads(requests.get(base_url, headers=self.headers).text)
        list = []
        self.course_name = response['data']['course_name']
        for item in response['data']['course_chapter']:
            for course in item['section_leaf_list']:
                if course.get('leaf_list', None) == None:
                    list.append(dict(course))
                else:
                    for course_item in course['leaf_list']:
                        course_item['name'] = course['name'] + course_item['name']
                        list.append(course_item)

        return list

    def get_course_list_info(self, course_list: list, cid, sign):
        base_url = f"https://www.xuetangx.com/api/v1/lms/learn/leaf_info/{cid}/{'{}'}/?sign={sign}"
        list = []
        for course in course_list:
            id = course['id']
            response = json.loads(requests.get(base_url.format(id), headers=self.headers).text)


            if response['data']['content_info']['media'].get('ccid', None) == None or response['data']['content_info']['media'].get('ccid', None) == '':
                continue

            print(course['name'])
            list.append({'name': course['name'], 'ccid': response['data']['content_info']['media']['ccid']})
        return list

    def download_subscript(self, course_list_info: list):
        base_url = "https://www.xuetangx.com/api/v1/lms/service/subtitle_parse/?c_d={}"
        with tqdm(course_list_info) as course_list_info:
            for course in course_list_info:
                course_list_info.set_postfix_str(course['name'])
                path = os.path.join(self.save_path, self.course_name)

                if not os.path.isfile(os.path.join(path, course['name'] + '.txt')):
                    response = json.loads(requests.get(base_url.format(course['ccid']), headers=self.headers).text)
                    # skip the video without subscription
                    if response.get('start', None) == None:
                        continue
                    start = response['start']
                    end = response['end']
                    text = response['text']

                    if not os.path.isdir(path):
                        os.mkdir(path)

                    with open(os.path.join(path, course['name'] + '.txt'), 'w', encoding='utf-8') as f:
                        for i in range(len(start)):
                            f.write(f"{start[i]} {end[i]} {text[i]}\n")
                else:
                    logger.info(f"{os.path.join(path, course['name'] + '.mp4')} is existed.")

    def download_video(self, course_list_info):
        base_url = "https://www.xuetangx.com/api/v1/lms/service/playurl/{}/?appid=10000"
        with tqdm(course_list_info) as course_list_info:
            for course in course_list_info:
                course_list_info.set_postfix_str(course['name'])
                path = os.path.join(self.save_path, self.course_name)
                # skip  video files has downloaded
                if not os.path.isfile(os.path.join(path, course['name'] + '.mp4')) and not os.path.isfile(os.path.join(path, course['name'] + '.wav')):
                    response = json.loads(requests.get(base_url.format(course['ccid']), headers=self.headers).text)
                    try:
                        # skip something weird exception
                        url = response['data']['sources']['quality10'][0]

                        if not os.path.isdir(path):
                            os.mkdir(path)
                        self.download_video_from_url(url, os.path.join(path, course['name'] + '.mp4'))

                    except KeyError as e:
                        logger.error(f"{course['name']} have no subscription")
                else:
                    logger.info(f"{os.path.join(path, course['name'] + '.mp4')} is existed.")

    def download(self, cid, sign):
        self.join_course(cid, sign)
        course_list = dl.get_course_list(cid, sign)
        course_list_info = dl.get_course_list_info(course_list, cid, sign)

        self.download_video(course_list_info)
        self.download_subscript(course_list_info)


if __name__ == '__main__':
    dl = xuetangx()
    list = [
        # ('5894455', 'ncepu0301zw'),# 民法典时代的典型合同与生活， 已下载
        # ('5881551', 'HEU03031001316'),# 古典社会学理论(2021春)
        # ('5883325', 'GZHU01011001428'), #西方哲学经典赏析
        # ('5881414', 'THU01011000406'), #西方思想经典与现代社会(2021春)
        # ('5881466', 'jnu03051000682'), #走进马克思，已下载，没有字幕
        # ('5881326', 'THU12011001060'), #逻辑学概论
        # ('5881418', 'THU03051000744'), # 习近平新时代中国特色社会主义思想
        # ('5881759', 'NJU01011001027'), #民法典时代的典型合同与生活
        # ('5883780', 'gzu04011002436'), #王阳明与贵州文化(2021春)
        # ('5881396', 'NJU01011000229'), # 理解马克思
        # ('5843741', 'scst02011003727'), # 客户关系管理
        # ('5882815', 'THU04011000365'), # 如何写好科研论文(2021春)
        # ('5882876', 'THU03051000392'), # 思想道德修养与法律基础(2021春)
        # ('5882701', 'CQU01011001311'),# 智慧的秘密
        # ('5882995', 'HENANNU01011000772'), # 儒释道哲学的人生智慧
        # ('5883381', 'xnkj01011002044'),# 逻辑学
        # ('3987757', 'thu1208355002894'),
        # ('5882458', 'CUC01011001092'),
        # ('5883274', 'FDU02031000062'), # 货币金融学(2021春)
        # ('5882819', 'THU02041000368'), # 商学导论：10节课带你走进商业世界
        # ('5882479', 'THU02031000333'), # 金融工程导论
        # ('5882677', 'RUC02011000591'), # 微观经济学原理（先修课）
        # ('5878771', 'THU13011000261'), # 不朽的艺术：走进大师与经典
        #('5882950', 'THU13011000408'), #现代生活美学——插花之道
        #('5882396', 'THU13051000381'), #视觉传达设计思维与方法
        ('5883041', 'THU10021000448'), #走进医学
        ('5882866', 'JNU10051000164'), #中医与诊断-学做自己的医生
        ('5882171', 'SEU10051000059'), #中医养生方法学
        ('5882813', 'PKU10041000675') # 身边的营养学

            ]
    for item in list:
        dl.download(item[0], item[1])
    # dl.download('5881358', 'THU01011000366')