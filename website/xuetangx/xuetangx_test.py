# -*- coding: utf-8 -*-
# @Time  : 2021/3/18 10:55
# @Author : lovemefan
# @File : test.py
# -*- coding: utf-8 -*-
# @Time  : 2021/3/16 19:47
# @Author : lovemefan
# @File : xuetanzaixian.py
import subprocess
import sys
import os
import re
from time import sleep
import requests
from tqdm import tqdm
import json
from bs4 import BeautifulSoup



class xuetangx():

    def __init__(self, *base_dirs):
        # todo 修改cookie值 和 save_path保存路径
        self.headers = {
                            "cookie": "provider=xuetang; django_language=zh; _ga=GA1.2.1070881427.1615894932; _gid=GA1.2.1120574251.1615894932; login_type=WX; csrftoken=Suf7suanEuttxHfINy6btjNdMvWHcjwJ; sessionid=hk2htylts3wrgb7dsesqd6gdpw8rq5f8; k=32717444; _gat_gtag_UA_164784773_1=1",
                            "xtbz": "xt"
                        }

        self.save_path = "F:\pythonProject\speechDataSetCrawler\data"
        self.course_name = ''

    def join_course(self, cid, sign):
        base_url = f"https://www.xuetangx.com/api/v1/lms/product/sku_pay_detail/?cid={cid}&sign={sign}"
        result = json.loads(requests.get(base_url).text)
        product_id = result['data']['product_id']
        sku_id = result['data']['sku_info'][0]['sku_id']
        url = f"https://www.xuetangx.com/api/v1/lms/order/entries_free_sku/{product_id}/?sid={sku_id}"
        result = json.loads(requests.get(url, headers=self.headers).text)
        print(f"加入课堂{'成功' if result['success'] else '失败'}")

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

    def get_course_list_info(self, course_list, cid, sign):
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

    def download_subscript(self, course_list_info):
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
                    print(f"{os.path.join(path, course['name'] + '.mp4')} is existed.")

    def download_video(self, course_list_info):
        base_url = "https://www.xuetangx.com/api/v1/lms/service/playurl/{}/?appid=10000"
        for course in course_list_info:
            path = os.path.join(self.save_path, self.course_name)
            # skip  video files has downloaded
            if not os.path.isfile(os.path.join(path, course['name'] + '.mp4')):
                response = json.loads(requests.get(base_url.format(course['ccid']), headers=self.headers).text)
                try:
                    # skip something weird exception
                    url = response['data']['sources']['quality10'][0]

                    if not os.path.isdir(path):
                        os.mkdir(path)
                    self.download_video_from_url(url, os.path.join(path, course['name'] + '.mp4'))
                except KeyError as e:
                    print(f"{course['name']} have no subscription")
            else:
                print(f"{os.path.join(path, course['name'] + '.mp4')} is existed.")

    def download(self, cid, sign):
        # join the course
        self.join_course(cid, sign)
        course_list = dl.get_course_list(cid, sign)
        course_list_info = dl.get_course_list_info(course_list, cid, sign)
        self.download_video(course_list_info)
        self.download_subscript(course_list_info)

    def download_video_from_url(self, url, file_path):
        """下载二进制文件"""
        cnt = 0
        RE_SPEED = re.compile(r'\d+MiB/(\d+)MiB\((\d+)%\).*?DL:(\d*?\.?\d*?)([KM])iB')
        RE_AVESPEED = re.compile(r'\|\s*?([\S]*?)([KM])iB/s\|')
        LENGTH = 80

        dir_name = os.path.dirname(file_path)
        file_name = file_path.split('\\')[-1] if sys.platform == 'win32' else file_path.split('/')[-1]
        aira2_cmd = f'aria2c  --header "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 -- fUcIvJ01pZVQhNq23lXm9gjazkeonsCx" --check-certificate=false -x 16 -s 64 -j 64 -k 2M --disk-cache 128M "{url}" -d "{dir_name}" -o "{file_name}"'
        while cnt < 3:
            try:
                p = subprocess.Popen(aira2_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True,
                                     encoding='utf8')
                lines = ''
                while p.poll() is None:
                    line = p.stdout.readline().strip()
                    if line:
                        lines += line
                        match = RE_SPEED.search(line)
                        if match:
                            size, percent, speed, unit = match.groups()
                            percent = float(percent)
                            speed = float(speed)
                            if unit == 'K':
                                speed /= 1024
                            per = min(int(LENGTH * percent / 100), LENGTH)

                            print(
                                '\r|-[' + per * '█' + (LENGTH - per) * '.' + '] {} {:.0f}% {:.2f}M/s'.format(file_name,
                                                                                                             percent,
                                                                                                             speed),
                                end=' (ctrl+c中断)')
                if p.returncode != 0:
                    cnt += 1
                    if cnt == 1:
                        self.clear_files(file_path, file_name)
                        sleep(0.16)
                else:
                    if file_name.endswith('.mp4'):
                        match = RE_AVESPEED.search(lines)
                        if match:
                            ave_speed, unit = match.groups()
                            ave_speed = float(ave_speed)
                            if unit == 'K':
                                ave_speed /= 1024

                        print('\r|-[' + LENGTH * '█' + '] {} {:.0f}% {:.2f}M/s'.format(file_name, 100, ave_speed),
                              end='  (完成)    \n')
                    return
            finally:
                p.kill()  # 保证子进程已终止
        self.clear_files(dir_name, file_name)

    def clear_files(self, dirname, filename):
        filepath = os.path.join(dirname, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        if os.path.exists(filepath + '.aria2'):
            os.remove(filepath + '.aria2')


if __name__ == '__main__':
    dl = xuetangx()
    # 根据链接 例如：https://www.xuetangx.com/learn/thu1202fu0623012/thu1202fu062301/5884222
    # 其中thu1202fu0623012为sign，5884222为cid，需要手动加入课程，或者自己抓一下加入课程的接口
    list =[('5881396', 'NJU01011000229')]
    for item in list:
        dl.download(item[0], item[1])
    # dl.download('5881358', 'THU01011000366')