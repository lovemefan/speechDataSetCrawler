
# -*- coding: utf-8 -*-
# @Time  : 2021/7/21 13:58
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : gtts.py

from gtts import gTTS
tts = gTTS('hello')
tts.save('hello.mp3')