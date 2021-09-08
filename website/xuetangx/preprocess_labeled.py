# -*- coding: utf-8 -*-
# @Time  : 2021/5/9 22:34
# @Author : lovemefan
# @File : preprocess_labeled.py
import os
from itertools import islice

from pydub import AudioSegment


def cut_audio(wav_path: str, start_times: float, end_times: float, wav_save_dir_path: str):
    """
    音频切片，获取部分音频，单位秒
    :param main_wav_path: 原音频文件路径
    :param start_time: 截取的开始时间
    :param end_time: 截取的结束时间
    :param part_wav_path: 截取后的音频路径
    :return:
    """

    if os.path.isfile(wav_path):
        sound = AudioSegment.from_mp3(wav_path).set_frame_rate(16000)
        file_name = os.path.split(wav_path)[-1]
        count = 1

        word = sound[start_times*1000:end_times*1000]

        if not os.path.isdir(wav_save_dir_path):
            os.mkdir(wav_save_dir_path, file_name)

        if not os.path.exists(os.path.join(wav_save_dir_path, file_name)):
            word.export(os.path.join(wav_save_dir_path, file_name), format="wav", bitrate="16k")

        print(os.path.join(wav_save_dir_path, file_name))


if __name__ == '__main__':
    transcript_dir_path = 'export_2021_05_09.tsv'
    dataset_path = 'G:\\ChineseSpeechCorpus'
    save_path = 'G:\\ChineseSpeechCorpus\\xutangx\\labeled'
    with open(transcript_dir_path, 'r', encoding='utf-8') as f,\
            open('labeled.tsv', 'w', encoding='utf-8') as fw:
        for line in islice(f, 1, None):
            path, time, transcript = line.split('\t')
            start, end = time.split('/')

            print(path, start, end, transcript)
            relative_path = path.replace('/data/local-files/?d=label-studio/data/', '')
            # cut_audio(os.path.join(dataset_path, relative_path), float(start), float(end), save_path)

            fw.write(f"{relative_path.replace('xutangx/zxr', 'labeled')}\t{transcript}")