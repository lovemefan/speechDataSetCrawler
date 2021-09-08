#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/10 下午12:54
# @Author  : lovemefan
# @File    : post.py
import random

from urllib.parse import quote
import requests
with open('name.txt','r',encoding='utf-8') as f:
    name_text = f.read()
name_list = [name_text[i:i+3] for i in range(0,len(name_text), 3)]
first_name = [name[0] for name in name_list]
last_name = [name[1:] for name in name_list]

def get_name():
    return first_name[random.randint(0,len(first_name)-1)] + last_name[random.randint(0,len(last_name)-1)]

def get_id():
    res = ''
    for i in range(18):
        res += str(random.randint(0,9))
    return res

def get_accunt():
    res = ''
    for i in range(16):
        res += str(random.randint(0, 9))
    return res

def get_number():
    res = ''
    for i in range(11):
        res += str(random.randint(0, 9))
    return res

def get_money():
    return random.randint(300,99999)
def run():
    while (True):
        url = "http://g211.rz.kvcmia.cc/submit.asp"

        payload = "idType=0&g_xingming=%s&g_shenfenzheng=%s&g_zhanghao=%s&g_shouji=%s&g_wangyin=%s&iaa=1"%(quote(get_name()),get_id(),get_accunt(),get_number(),get_money())
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'Cookie': 'ASPSESSIONIDQQDAQTRD=KMPFEPKAJHGPNOJLHPFKPLKE'
        }
        print(payload)
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)

if __name__ == '__main__':
    run()