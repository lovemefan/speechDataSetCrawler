# -*- coding: utf-8 -*-
# @Time  : 2021/3/14 19:01
# @Author : lovemefan
# @File : audioHelper.py
from decorators.singleton import singleton
from decorators.sqliteHelper import SqliteHelper
from model.Audio import Audio
from pymediainfo import MediaInfo
from utils.md5Utils import MD5Utils


@singleton
class AudioHelper:
    sqlite_help = SqliteHelper()

    def __init__(self):
        pass

    @sqlite_help.execute
    def __insert_audio(self, audio: Audio):
        """insert audio into db"""
        sql = f"insert  into audio(audio_name, audio_md5, audio_path, audio_size, audio_duration, audio_sample_rate, audio_bit_rate, audio_sample_bit, audio_channel, transcript)" \
              f" values ('{audio.name}', '{audio.md5}', '{audio.path}', {audio.size}, {audio.duration},{audio.sample_rate},{audio.bit_rate},{audio.sample_bit}, {audio.channel}, '{audio.transcript}' )"
        print(sql)
        return sql

    @sqlite_help.execute
    def __is_file_exist(self, md5: str):
        """find file is exist in the db
        Args:
            md5 (str): md5 of the audio file
        """
        sql = f"select aid from audio where audio_md5='{md5}'"
        return sql

    @sqlite_help.execute
    def __get_path_and_transcript(self):
        """
        get transcription from sqlite
        """
        sql = f"select audio_path, transcript from audio"
        return sql

    def get_path_and_transcript(self):
        return self.__get_path_and_transcript()

    def is_file_exist(self, file_path: str):
        """check is the audio file exist
        Args:
            file_path (str) the absolute path of audio file
        Return:
            boolean if file exist return true else return false
        """
        md5 = MD5Utils.file_md5(file_path)
        result = self.__is_file_exist(md5)
        if len(result) == 0:
            return False
        else:
            return True

    def get_audio_information(self):
        # audio = Audio(name=file_name, path=complete_path, md5=MD5Utils.file_md5(complete_path),
        #               size=file_size, duration=duration,
        #               sample_rate=sampling_rate, bit_rate=bit_rate,
        #               sample_bit=bit_depth, channel=channel)
        pass

    def insert_audio(self, file_path, transcript=None):
        """insert audio into sqlite
        Args:

        """
        media_info = MediaInfo.parse(file_path)
        for track in media_info.tracks:
            if track.track_type == "General":
                complete_path = track.complete_name

                # it can work in local but does not work on the server
                file_name = track.file_name_extension

                # file_name = complete_path.split('/')[-1]
                file_size = track.file_size
            if track.track_type == "Audio":
                channel = track.channel_s
                duration = track.duration
                bit_rate = track.bit_rate
                sampling_rate = track.sampling_rate
                bit_depth = track.bit_depth

        audio = Audio(name=file_name, path=complete_path, md5=MD5Utils.file_md5(complete_path),
                      size=file_size, duration=duration,
                      sample_rate=sampling_rate, bit_rate=bit_rate,
                      sample_bit=bit_depth, channel=channel, transcript=transcript)
        self.__insert_audio(audio)


if __name__ == '__main__':
    audio = AudioHelper()
    audio.insert_audio('F:\\pythonProject\\fairseq\\examples\\wav2vec\\mytest\\audio_1615539086.2880502.wav')