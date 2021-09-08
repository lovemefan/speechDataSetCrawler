# -*- coding: utf-8 -*-
# @Time  : 2021/3/14 16:49
# @Author : lovemefan
# @File : AudioDownloader.py
import abc
import os
import platform
import re
import subprocess
import sys
from time import sleep

import requests
from tqdm import tqdm

from utils.audioHelper import AudioHelper
from utils.log import logger


class MediaDownloader(metaclass=abc.ABCMeta):
    '''Base class of audio downloader to down audio from diffrent website'''

    def __init__(self):
        self.__audio_helper = AudioHelper()
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/71.0.3578.80 Safari/537.36'}

    def insert_audio(self, file_path):
        """insert a audio into db"""
        self.__audio_helper.insert_audio(file_path)

    def download_audio_from_urls(self, urls, file_path: str):
        """download one audio file
        you must overwrite this method to fit different websit
        :param urls: the url of audio, url could be str or list of url
        :param file_path: the save path of audio file
        :return: str： must be absolute file path of audio file
        """
        if type(urls) == str:
            urls = [urls]
        with tqdm(urls) as urls:
            for url in urls:
                response = requests.get(url)
                with open(file_path, 'wb') as f:
                    f.write(response.content)

                file_name = file_path.split('\\')[-1] if platform.system() == 'Windows' else file_path.split('/')[-1]

                urls.set_postfix_str(file_name)
                logger.info(f"{file_name} download finished")
                # insert into db
                # todo check file exist
                file_exist = self.__audio_helper.is_file_exist(file_path)
                if file_exist:

                    logger.warning(f'{file_name} is exist')
                else:
                    self.insert_audio(file_path)

    def download_video_from_url(self, url, file_path):
        """下载二进制文件"""
        self.download_media_from_url(url, file_path)

    def download_media_from_url(self, url, file_path):
        cnt = 0
        RE_SPEED = re.compile(r'\d+MiB/(\d+)MiB\((\d+)%\).*?DL:(\d*?\.?\d*?)([KM])iB')
        RE_AVESPEED = re.compile(r'\|\s*?([\S]*?)([KM])iB/s\|')
        LENGTH = 80

        dir_name = os.path.dirname(file_path)
        file_name = file_path.split('\\')[-1] if sys.platform == 'win32' else file_path.split('/')[-1]
        aira2_cmd = f'aria2c  --header "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 -- fUcIvJ01pZVQhNq23lXm9gjazkeonsCx" --check-certificate=false -x 16 -s 64 -j 64 -k 2M --disk-cache 128M "{url}" -d "{dir_name}" -o "{file_name}"'
        while cnt < 3:
            try:
                p = subprocess.Popen(aira2_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True, encoding='utf8')
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
                                '\r|-[' + per * '█' + (LENGTH - per) * ' ' + '] {} {:.0f}% {:.2f}M/s'.format(file_name,
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


class FileExist(Exception):
    def __init__(self, file_name):
        self.username = file_name

    def __str__(self):
        return f"file '{self.file_name}' is already exist"


if __name__ == '__main__':
    download = MediaDownloader()
    download.download_audio_from_urls('http://sound2.yywz123.com/english96ad/lesson/nce1/sound/184faabcdfceebd.mp3', '1.mp3')