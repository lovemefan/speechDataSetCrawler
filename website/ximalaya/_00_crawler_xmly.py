import re
from concurrent.futures.thread import ThreadPoolExecutor

import requests
import os
import json
import argparse

import utils


def get_response(html_url):
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        # 'Cookie':'_xmLog=h5&15936d0e-f90d-4641-85a2-8d1ea0b35c5a&2.2.17; x_xmly_traffic=utm_source%3A%26utm_medium%3A%26utm_campaign%3A%26utm_content%3A%26utm_term%3A%26utm_from%3A; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1615955470,1615955666,1616028334; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1616028862'
    }
    response = requests.get(url=html_url, headers=header)
    return response


def alter_title(title):

    ## 去除空格
    title_modified = title.replaceAll(" ", "_")

    ## 有数字，数字替换 -4位占位符 // 默认只处理一个数字的情况
    pattern = r'\d+'
    str_list = re.findall(pattern, title_modified)
    title_modified = title_modified.replaceAll(str_list[0], "%04d"%int(str_list[0]))

    # ## 无数字，“第二十八章”替换 - 4位占位符
    # pattern_hz = r'[第]([\u4e00-\u9fa5]+)[章集]'
    # chapter_hz_list = re.findall(pattern_hz,title_modified)
    # if len(chapter_hz_list) > 0 :
    #     chapter_hz = chapter_hz_list[0]
    #     chapter_sz = utils.chinese2digits(chapter_hz.encode('gbk').decode('cp936'))
    #     title_modified = title_modified.replace(chapter_hz,"%04d"%chapter_sz)

    return title_modified

def download_and_save(dir, title, audio_url):
    if not os.path.exists(dir):
        os.makedirs(dir)
    audio_content = get_response(audio_url).content

    title_modified = alter_title(title)

    with open(os.path.join(dir, title_modified + '.m4a'), mode='wb') as f:
        f.write(audio_content)
        print('正在保存：new name:%s \n\t old name:%s \n\n'%(title_modified,title))
    return 0


def get_audio_info(html_url):

    audio_info_list = []
    content = json.loads(get_response(html_url).text)
    jlist = content['data']['trackDetailInfos']

    for li in jlist:

        # 音频ID
        audio_id = li['id']
        # 章节名字
        audio_title = li['trackInfo']['title']
        # 下载地址
        audio_url = li['trackInfo']['playPath']

        audio_info = []
        audio_info.append(audio_id)
        audio_info.append(audio_title)
        audio_info.append(audio_url)

        audio_info_list.append(audio_info)
    return audio_info_list

    # albumids = ['30748094','23085924','4756811','33620874']
    # dirs = ['月亮与六便士','巴黎圣母院','摸金天师','海底两万里','鬼吹灯']



parser = argparse.ArgumentParser()
parser.add_argument("--save_root", default="F:\\xmly", type=str)


def main():
    pool = ThreadPoolExecutor(max_workers=10)
    args = parser.parse_args()
    pagesize = 50

    thread_list = []
    for album_id, album_name in utils.read_album_json("album.json"):

        # get audio_info of a album
        page = 1
        audio_info_list = []
        while True:
            url = f'https://m.ximalaya.com/m-revision/common/album/queryAlbumTrackRecordsByPage?albumId={album_id}&page={page}&pageSize={pagesize}&asc=true&countKeys=play%2Ccomment&v=1616033847338'
            temp_list = get_audio_info(url)
            if len(temp_list) > 0:
                audio_info_list += temp_list
                page += 1
            else:
                break

        # download & save
        for li in audio_info_list:
            file_path = os.path.join(args.save_root, album_name, "origin")
            trd = pool.submit(download_and_save, file_path, li[1], li[2])
            thread_list.append(trd)
            print("Thread added: %s"  % file_path)
            # download_and_save(os.path.join(args.save_root, album_name, "origin"), li[1], li[2])
    print([i.result() for i in thread_list])
    pool.shutdown()
## 下载文件名-空格替换
## 章节数有序 - 占位
if __name__ == '__main__':

    main()

