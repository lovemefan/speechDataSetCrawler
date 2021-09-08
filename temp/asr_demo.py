# -*- coding: utf-8 -*-
# @Time  : 2021/7/20 15:23
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : asr_demo.py


import time
import wave
import socketio

sio = socketio.Client()

@sio.event
def connect():

    print('connection established')


@sio.on('server_response')
def server_response(data):
    print('server_response', data)

    # sio.emit('my response', {'response': 'my response'})


@sio.on('server_partial_response')
def server_partial_response(data):
    print('server_partial_response', data)
    # mylog.info(f'server_response: {data}')


@sio.on('server_response_end')
def server_response_end(data):
    print('server_response_end', data)
    print(f'server_response: {data}')
    if data['data'] == '正常！':
        sio.disconnect()

    if data['data'] == '超时！':
        # 超时一定要关掉连接
        sio.disconnect()


@sio.on('error')
def error(data):
    print('error', data)
    sio.disconnect()
    print(f'当前测试语音识别：出现异常{data}')



@sio.event
def disconnect():
    print('disconnected from server')


def testSocket(file, language_code, http):
    """测试socket接口
    :param file: 音频文件路径
    :param language_code: 音频语言代码
    :return:
    """

    wf = wave.open(file, 'rb')
    # print(wf.getparams())
    data = wf.readframes(wf.getnframes())


    wf.close()
    # 等待上一个测试
    sio.wait()
    past = time.time()
    print(http)
    sio.connect(http)
    sio.emit('connect_event', {'language_code': language_code, 'sample_rate': '16000'})

    sio.emit('voice_push_event', {"voiceData": data})
    sio.emit('voice_push_event', {"voiceData": "EOF"})

    # wait until the connection with the server ends
    sio.wait()
    now = time.time()
    print(f"响应时间：{now - past}s")

    # 响应时间超时,超过5s就超时
    if now - past > 5:
        print(f'当前测试语音识别：响应超时{now - past}s')
        # res['data'] = {"error": f"当前测试{cur_lang}语音识别：响应超时{now - past}s"}


if __name__ == '__main__':
    testSocket("越南语.wav", 'vi-VN', 'http://8.129.171.64:5100')

