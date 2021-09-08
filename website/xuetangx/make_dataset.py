# -*- coding: utf-8 -*-
# @Time  : 2021/3/18 13:04
# @Author : lovemefan
# @File : make_dataset.py
import os
import shutil
import sys
import time

from pymediainfo import MediaInfo
from tqdm import tqdm

from utils.snowflake import IdWorker

print(os.getcwd())
sys.path.append(os.getcwd())
from utils.audioHelper import AudioHelper

sys.path.append(os.path.dirname(os.path.abspath(os.pardir)))
print(os.path.dirname(os.path.abspath(os.pardir)))
from pydub import AudioSegment

from moviepy.video.io.VideoFileClip import VideoFileClip

from config.Config import Config


class DatasetMaker:
    def __init__(self):
        #todo mp4_path: 视频路径， dataset_path：切好后存放路径， transcript_path：切好后字幕存放路径
        self.mp4_path = Config.get_instance().get('file.save_path')
        self.dataset_path = Config.get_instance().get('file.data_set')
        self.transcript_path = Config.get_instance().get('file.transcript_path')
        self.allpath = []
        self.allname = []
        self.audio_helper = AudioHelper()
        # self.get_all_file(self.mp4_path)


    def mp4towav(self, file_path: str):
        # file_name = file_path.split('\\')[-1] if sys.platform == 'win32' else file_path.split('/')[-1]
        if not os.path.isfile(file_path.replace('.mp4', '.wav')):
            if not os.path.isfile(file_path.replace('.mp4', '.mp4.aria2')):
                video = VideoFileClip(file_path)
                audio = video.audio
                audio.write_audiofile(file_path.replace('.mp4', '.wav'))
                audio.close()
                video.close()
                os.remove(file_path)
        else:
            os.remove(file_path)

    def __getallfile(self, path):
        allfilelist = os.listdir(path)
        # 遍历该文件夹下的所有目录或者文件
        for file in allfilelist:
            filepath = os.path.join(path, file)
            # 如果是文件夹，递归调用函数
            if os.path.isdir(filepath):
                self.__getallfile(filepath)
            # 如果不是文件夹，保存文件路径及文件名
            elif os.path.isfile(filepath):
                self.allpath.append(filepath)
                self.allname.append(file)

        return self.allpath, self.allname

    def get_all_file(self, path):
        return self.__getallfile(path)

    def convertion(self):

        for path in self.allpath:
            if path.endswith("mp4"):
                self.mp4towav(path)

    def cut_audio(self, wav_path: str, start_times: list, end_times: list, part_wav_dir_path, transriptions):
        """
        音频切片，获取部分音频，单位秒
        :param main_wav_path: 原音频文件路径
        :param start_time: 截取的开始时间
        :param end_time: 截取的结束时间
        :param part_wav_path: 截取后的音频路径
        :return:
        """
        if not os.path.isfile(wav_path.replace('wav', 'finished.wav')):
            if os.path.isfile(wav_path):
                sound = AudioSegment.from_mp3(wav_path).set_frame_rate(16000)
                file_name = os.path.split(wav_path)[-1].replace('.wav', '')
                count = 1
                assert len(start_times) == len(end_times)
                length = len(start_times)
                with open(self.transcript_path, 'a', encoding='utf-8') as f:
                    for i in range(length):

                        word = sound[int(float(start_times[i]) - 200):int(float(end_times[min(i, length - 1)]))]
                        if not os.path.isdir(os.path.join(part_wav_dir_path, file_name)):
                            os.mkdir(os.path.join(part_wav_dir_path, file_name))
                        word.export(os.path.join(part_wav_dir_path, file_name, f"{count}.wav"), format="wav", bitrate="16k")
                        # 插入sqlite数据库， 可以不要

                        self.audio_helper.insert_audio(os.path.join(part_wav_dir_path, file_name, f"{count}.wav"), transriptions[i].replace("'", ''))
                        print(os.path.join(part_wav_dir_path, file_name, f"{count}.wav"))
                        f.write(f'{os.path.join(part_wav_dir_path, file_name, f"{count}.wav")} , {transriptions[i]}\n')
                        count = count + 1

    def labeled(self):

        for path in self.allpath:
            dir_name = os.path.split(os.path.dirname(path))[-1]
            dir_path = os.path.join(self.dataset_path, dir_name)

            starts = []
            ends = []
            transriptions = []
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            if path.endswith('txt'):
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read().split('\n')
                    for line in text:
                        content = line.split(' ')
                        if len(content) == 3:
                            start, end, transription = line.split(' ')
                            starts.append(start)
                            ends.append(end)
                            transriptions.append(transription)
                if not os.path.isfile(path.replace('.txt', '.finished.wav')):
                    self.cut_audio(path.replace('txt', 'wav'), starts, ends, dir_path, transriptions)
                    if os.path.isfile(path.replace('txt', 'wav')):
                        os.rename(path.replace('txt', 'wav'), path.replace('.txt', '.finished.wav'))

    def export_txt_file(self):
        results = self.audio_helper.get_path_and_transcript()
        with open('transcipt.txt', 'w', encoding='utf-8') as f:
            with tqdm(results) as results:
                for item in results:
                    path = item[0].replace('F:\\pythonProject\\speechDataSetCrawler\\dataset\\', '')
                    f.write(f"{path}\t{item[1]}\n")


    def flush_file(self):
        file_path_read = 'H:\\ChineseSpeechCorpus\\all_wav.lst'
        file_oath_write = 'H:\\ChineseSpeechCorpus\\zxr_wav.lst'
        with open(file_path_read, 'r', encoding='utf-8') as f_read:
            list = f_read.read()

        list = list.split('\n')
        with open(file_oath_write, 'w', encoding='utf-8') as f_write:
            for index, item in enumerate(list):
                try:
                    path, transcript = item.split('\t', 1)
                    path = path.replace('F:\\xtzx\\', '')
                    transcript = transcript.strip()
                    f_write.write(f"{path}\t{transcript}\n")
                except Exception as e:
                    print(e)
                    print(item, index)


    def collect_all_data(self):
        """收集整理所有人的音频"""
        wav_list = [
            # 'G:\\ChineseSpeechCorpus\\labelld\\jl\\wav.lst',
            # 'G:\\ChineseSpeechCorpus\\labelld\\st\\wav.lst',
            # 'H:\\ChineseSpeechCorpus\\labelld\\oyf\\wav.lst',
            # 'H:\\ChineseSpeechCorpus\\labelld\\zlf\\wav.lst',
            # 'H:\\ChineseSpeechCorpus\\labelld\\wjq\\wav.lst'
            'H:\\ChineseSpeechCorpus\\labelld\\zxr\\wav.lst'
            ]
        source_root = os.path.dirname(wav_list[0])
        target_root = 'H:\\ChineseSpeechCorpus\\xutangx'
        with open('H:\\ChineseSpeechCorpus\\all_wav.lst', 'a', encoding='utf-8') as fw:

            for item in wav_list:
                with open(item, 'r', encoding='utf-8') as f:
                    content = f.read()
                content = content.split('\n')
                with tqdm(content) as content_tqmd:
                    for index, line in enumerate(content_tqmd):
                        try:
                            path, transcript = line.split('\t', 1)
                            source_absolute_path = os.path.join(source_root, path)
                            file_name = f"{time.strftime('%Y%m%d')}_{IdWorker().get_id()}.wav"
                            file_dir_name = item.split('\\')[-2]
                            dir_absolute_path = os.path.join(target_root, file_dir_name)
                            if not os.path.isdir(dir_absolute_path):
                                os.mkdir(dir_absolute_path)

                            target_absolute_path = os.path.join(dir_absolute_path, file_name)

                            if os.path.exists(source_absolute_path):
                                fw.write(f"{os.path.join(file_dir_name, file_name)}\t{transcript}\n")
                                shutil.move(source_absolute_path, target_absolute_path)
                        except:
                            print(item, line, index)





    def analysis_labelled(self):
        """统计一下任务时长"""
        file_path = 'H:\\ChineseSpeechCorpus\\xutangx\\all_wav.lst'
        root_path = 'H:\\ChineseSpeechCorpus\\xutangx'
        total_time_count = 0



        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.split('\n')
        time_count = {
            'st': 0,
            'oyf': 0,
            'zxr': 0,
            'zlf': 0,
            'wjq': 0,
            'jl': 0,
        }


        with tqdm(content) as content:
            for line in content:

                path, transcript = line.split('\t', 1)
                name = path.split('\\')[0]

                wav_file_abosulte_path = os.path.join(root_path, path)
                if os.path.exists(wav_file_abosulte_path):
                    media_info = MediaInfo.parse(wav_file_abosulte_path)
                    for track in media_info.tracks:
                        if track.track_type == "Audio":
                            duration = track.duration
                            if type(duration) == int:
                                time_count[name] += duration
                                total_time_count += duration
                            else:
                                12
                                pass

        print(time_count)
        print(total_time_count)

    def analysis_unlabelled(self):
        file_path = 'G:\\ChineseSpeechCorpus\\unlabelled\\pt\\cutted'
        print("loading files")
        self.get_all_file(file_path)
        time_count = {}
        print("load finished")
        with tqdm(self.allpath) as allpath:
            for file in allpath:
                owner = file.replace(file_path, '').split('\\')[0]

                if file.endswith('wav') or file.endswith('mp3'):
                    media_info = MediaInfo.parse(file)
                    for track in media_info.tracks:
                        if track.track_type == "Audio":
                            duration = track.duration
                            if type(duration) == int:
                                if time_count.get(owner, None):
                                    time_count[owner] += duration
                                else:
                                    time_count[owner] = duration

        print(time_count)
        for key, value in time_count:
            print(f"{key}: {int(value)/(1000*60*60)}")





    def validate_dataset(self):
        """验证一下标签是否有效，发现一些无效音频"""
        file_path = 'H:\\ChineseSpeechCorpus\\xutangx\\all_wav.lst'
        root_path = 'H:\\ChineseSpeechCorpus\\xutangx'
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.split('\n')
        time_count = 0
        file_count = 0
        with tqdm(content) as content:
            for index, line in enumerate(content):
                path, transcript = line.split('\t', 1)
                if not os.path.exists(os.path.join(root_path, path)):
                    print(path, index)

if __name__ == '__main__':
    ds = DatasetMaker()
    # ds.convertion()
    # ds.labeled()
    # ds.flush_file()
    # ds.export_txt_file()
    # ds.analysis()
    ds.analysis_unlabelled()
    # ds.collect_all_data()

    # ds.validate_dataset()