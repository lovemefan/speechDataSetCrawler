# -*- coding: utf-8 -*-
# @Time  : 2021/8/10 17:48
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : audio_cut.py
# -*- coding: utf-8 -*-
# @Time  : 2021/6/1 14:08
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : cut.py

import argparse
import json
import os
from pathlib import Path
import xlrd
from pydub import AudioSegment


def str2sec(x):
    '''
    字符串时分秒转换成秒
    '''
    h, m, s = x.strip().split(':')  # .split()函数将其通过':'分隔开，.strip()函数用来除去空格
    return int(h) * 3600 + int(m) * 60 + float(s)  # int()函数转换成整数运算


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='根据excel切割音频')
    parser.add_argument('--input_dir', required=True, metavar='INPUTWAVE',
                        help='the full path to input wave file')
    parser.add_argument('--output_dir', required=True, metavar='OUTPUTFILE',
                        help='the full path to output json file to save detected speech intervals')

    args = parser.parse_args()

    if os.path.isdir(args.input_dir):
        audios = Path(args.input_dir).glob("*.wav")
        if not os.path.exists(args.output_dir):
            os.mkdir(args.output_dir)
        for audio_path in audios:
            # pbar.update(1)
            audio_file = AudioSegment.from_file(audio_path)

            xls_file = os.path.join(audio_path).replace('.wav', '.xls')
            if not os.path.exists(xls_file):
                assert False, f"没有找到{xls_file} 文件"

            # 打开xls文件
            book = xlrd.open_workbook(xls_file)
            sheet = book.sheet_by_index(0)
            rows = sheet.nrows
            cols = sheet.ncols

            for index in range(1, rows):
                id = int(sheet.cell_value(index, 0))
                start = str2sec(sheet.cell_value(index, 1))*1000
                end = str2sec(sheet.cell_value(index, 2))*1000
                audio_file[start:end].export(os.path.join(args.output_dir, f"{audio_path.name}_{id}.wav"), format="wav")
