#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/7 下午8:00
# @Author  : lovemefan
# @File    : YoutubeCrawler.py
import json
import googleapiclient
from YoutubeDataApi import get_playlistItem, get_playlist

from website.youtube.YoutubeDataApi import get_caption

if __name__ == '__main__':
    """爬取某个channal的视频"""
    channal_name = 'UC7723FqVehXq2zeRb3tP0hQ'
    # 第一次请求，nextPageToken 参数为None
    nextPageToken_list = None
    play_listItem = []
    try:
        while True:
            play_list = get_playlist(channal_name, nextPageToken_list)
            # playlist 的分页参数
            nextPageToken_list = play_list.get('nextPageToken', '')
            for list in play_list['items']:

                nextPageToken_items = None
                while(True):
                    # 通过某一个播放列表的id取得播放列表里所有的视频信息
                    items = get_playlistItem(list['id'], nextPageToken_items)
                    # list item 的分页参数
                    nextPageToken_items = items.get('nextPageToken', '')
                    # 参看当前播放列表的信息
                    print(items['pageInfo'])
                    for item in items['items']:
                        try:
                            # 取出字幕信息
                            caption = get_caption(item['contentDetails']['videoId'])
                            # 如果有字幕
                            if len(caption['items']) != 0:
                                item['caption'] = caption['items']
                                # 字幕信息加入到视频信息中
                                play_listItem.append(item)
                        except googleapiclient.errors.HttpError:
                            # 遇到网络错误
                            continue
                    if nextPageToken_items == '':
                        break
            # 没有下一页了就结束
            if nextPageToken_list == '':
                break


        with open("data.json","w") as f:
            json.dump(play_listItem, f)
    except Exception as e:
        print(e)
        print(e.with_traceback())
        with open("data.json","w") as f:
            json.dump(play_listItem, f)

