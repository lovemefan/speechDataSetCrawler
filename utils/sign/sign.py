# -*- coding: utf-8 -*-
# @Time  : 2021/4/1 10:26
# @Author : lovemefan
# @File : sign.py
import argparse
import time

import requests
import schedule as schedule


def daily_sign(seq: int, token: str, sign_type=0):
    """日检日报打卡
    :param seq: 1为晨检，2为午检，3为晚检
    :param token: token需要抓包
    :param sign_type: 类型，0表示日检日报，1表示健康打卡
    """
    if sign_type == 0:
        url = 'https://student.wozaixiaoyuan.com/heat/save.json'
    else:
        url = 'https://student.wozaixiaoyuan.com/health/save.json'
    data = {
        "answers": "[\"0\"]",
        "seq": seq,
        "temperature": "36.1",
        "latitude": "24.852266",
        "longitude": "102.857704",
        "country": "中国",
        "city": "昆明市",
        "district": "呈贡区",
        "province": "云南省",
        "township": "吴家营街道",
        "street": "景明南路",
        "myArea": "呈贡校区",
        "areacode": "530114"
    }
    headers = {
        "Host": "student.wozaixiaoyuan.com",
        "Connection": "keep-alive",
        "Content-Length": "385",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        "content-type": "application/x-www-form-urlencoded",
        "token": token,
        "Referer": "https://servicewechat.com/wxce6d08f781975d91/168/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br"
    }

    response = requests.post(url, data=data, headers=headers)
    print(response.text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help='input you token', default='f1934170-351b-464b-b55f-1fabfcc3d457', required=True)
    args = parser.parse_args()

    # 健康打卡
    schedule.every().day.at("10:00").do(daily_sign, 1, args.token, sign_type=1)
    # 日检
    schedule.every().day.at("09:35").do(daily_sign, 1, args.token)
    # 午检
    schedule.every().day.at("15:05").do(daily_sign, 2, args.token)
    # 晚检
    schedule.every().day.at("21:35").do(daily_sign, 3, args.token)
    # 测试
    schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(5)
