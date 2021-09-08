#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/31 下午4:04
# @Author  : lovemefan
# @File    : Audio.py
class Audio:
    def __init__(self, name, md5=None, path=None, size=None, duration=None, sample_rate=None, bit_rate=None, sample_bit=None, channel=None, transcript=None):
        """class of audio

        :param name: audio name
        :param md5: audio file md5
        :param path: absolute path of audio
        :param size: audio file size
        :param uid: audio file duration in the unit of second
        :param sample_rate: sample_rate (Hz)
        :param bit_rate: bit_rate
        :param sample_bit: sample bit in the unit of bit peer second
        :param channel:1 is single channel,2 is dual-channel audio
        :param transcript: the transcript of audio
        """
        self.name = name
        self.md5 = md5
        self.path = path
        self.size = size
        self.duration = duration if duration else 0
        self.sample_rate = sample_rate
        self.bit_rate = bit_rate
        self.sample_bit = sample_bit if sample_bit else 'null'
        self.channel = channel
        self.transcript = transcript
