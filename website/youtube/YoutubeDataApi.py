#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/8 上午12:36
# @Author  : lovemefan
# @File    : YoutubeDataApi.py

import os

# pip install --upgrade google-api-python-client
import googleapiclient.discovery

# API_KEY = 'AIzaSyDMcVav2rRRJXtj0mSmoVq0llJ_Yq7xqOA'
API_KEY = 'AIzaSyCuH02lOjEYLVKQ5KggKqObcj4rTIMHvzM'



def get_playlist(channelId, pageToken=None):
    """获取播放列表
    :param channelId 频道id
    :param pageToken 分页的token
    """

    
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = API_KEY

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    if pageToken:
        request = youtube.playlists().list(
            part="id,contentDetails",
            channelId=channelId,
            maxResults=25,
            pageToken=pageToken
        )
    else:
        request = youtube.playlists().list(
            part="id,contentDetails",
            channelId=channelId,
            maxResults=25
        )
    response = request.execute()

    return response


def get_playlistItem(playlistId, pageToken=None):
    """获取播放列表中视频列表
    :param playlistId 播放列表id
    """
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = API_KEY

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    if pageToken:
        request = youtube.playlistItems().list(
            part="contentDetails,id",
            playlistId=playlistId,
            maxResults=25,
            pageToken = pageToken
        )
    else:
        request = youtube.playlistItems().list(
            part="contentDetails,id",
            playlistId=playlistId,
            maxResults=25,
        )
    response = request.execute()

    return response

def get_caption(videoId):
    """查看字幕情况"""
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = API_KEY

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.captions().list(
        part="snippet",
        videoId=videoId
    )
    response = request.execute()

    return(response)

if __name__ == '__main__':
    res = get_caption('4Fu1SXzCTeg')
    print(res)
