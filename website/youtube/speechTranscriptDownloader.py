#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/3 下午5:04
# @Author  : lovemefan
# @File    : speechTranscriptDownloader.py
import os
import sys
sys.path.append(os.path.abspath(os.pardir))
from utils import youtube_dl


def getSubtitleList(url, proxy=None):
    """获取youtube视频支持字幕的列表"""
    ydl_opts = {
        # 'proxy':'socks5://127.0.0.1:1080',
        'listsubtitles': url
    }
    if proxy:
        ydl_opts['proxy'] = proxy
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        res = ydl.extract_info(url, download=False)
    return res


def download(downurls:list, sub_lang:list, path=None, proxy=None):
    """下载音频和字幕
    :param downurls 下载列表，注意是列表
    :param sub_lang 字幕列表
    :param path 下载保存路径
    :param proxy 代理路径 例如 socks5://127.0.0.1:1080
    """
    if not downurls:
        raise ValueError('url is empty')



    ydl_opts = {
        'postprocessors': [{
           'key': 'FFmpegExtractAudio',
           'preferredcodec': 'wav',
        }],
        'subtitleslangs': sub_lang,
        'subtitlesformat': 'vtt'
    }
    if path:
        ydl_opts['outtmpl'] = path
    if  proxy:
        ydl_opts['proxy'] = proxy


    print(ydl_opts)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(downurls)
        # ydl.download(['https://www.youtube.com/watch?v=KaKq0UUTPU0&list=PLywfaJMr2okmMx9Ntlqq2YaEf7FQ8byq1'])


if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=7YkgHYElvso'
    res = getSubtitleList(url, 'socks5://127.0.0.1:1080')
    print(res)
    subtitleslangs = []
    for key,value in res.items():
        subtitleslangs.append(key)


    download([url],
             subtitleslangs,
             path='/media/lovemefan/Ubuntu 20.0/越南语/%(title)s.%(ext)s',
             proxy='socks5://127.0.0.1:1080')
