# -*- coding: utf-8 -*-
# @Time  : 2021/6/1 14:08
# @Author : lovemefan
# @Email : lovemefan@outlook.com
# @File : cut.py

import argparse
import json
import os
import auditok
from tqdm import tqdm

from utils.snowflake import IdWorker
from utils.vads import VoiceActivityDetector


def save_to_file(data, filename):
    with open(filename, 'w') as fp:
        json.dump(data, fp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Analyze input wave-file and save detected speech interval to json file.')
    parser.add_argument('--input_dir', metavar='INPUTWAVE',
                        help='the full path to input wave file')
    parser.add_argument('--output_dir', metavar='OUTPUTFILE',
                        help='the full path to output json file to save detected speech intervals')

    parser.add_argument('--min_dur', metavar='OUTPUTFILE', default=1.5)

    parser.add_argument('--max_dur', metavar='OUTPUTFILE', default=15)

    args = parser.parse_args()

    if os.path.isdir(args.input_dir):

        for path, dir_list, file_list in os.walk(args.input_dir):
            count = 0
            length = len(file_list)

            with tqdm(total=length) as pbar:
                for file_name in file_list:
                    pbar.update(1)
                    print(os.path.join(path, file_name))

                    if file_name.endswith('wav'):
                        # audio_bytes = open(os.path.join(path, file_name), 'rb').read()
                        # audio = auditok.AudioRegion(data=audio_bytes[44:], sampling_rate=16000, sample_width=2, channels=1)
                        try:
                            audio_regions = auditok.split(
                                os.path.join(path, file_name),
                                # audio,
                                min_dur=args.min_dur,  # minimum duration of a valid audio event in seconds
                                max_dur=args.max_dur,  # maximum duration of an event
                                max_silence=1.2,  # maximum duration of tolerated continuous silence within an event
                                energy_threshold=40  # threshold of detection
                            )
                        except EOFError:
                            continue

                        count += 1
                        id = str(hex(IdWorker().get_id())).replace('0x', '').replace('22000', '')
                        for i, r in enumerate(audio_regions):
                            # Regions returned by `split` have 'start' and 'end' metadata fields
                            # print("Region {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r))
                            filename = r.save(os.path.join(args.output_dir, id + "_{meta.start:.3f}-{meta.end:.3f}.wav"))
                            # print("Audio saved as: {}".format(filename))

    elif os.path.isfile(args.input_dir):

        # split returns a generator of AudioRegion objects
        audio_regions = auditok.split(
            args.input_dir,
            min_dur=args.min_dur,  # minimum duration of a valid audio event in seconds
            max_dur=args.max_dur,  # maximum duration of an event
            max_silence=0.3,  # maximum duration of tolerated continuous silence within an event
            energy_threshold=55  # threshold of detection
        )

        for i, r in enumerate(audio_regions):
            # Regions returned by `split` have 'start' and 'end' metadata fields
            print("Region {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r))

            # play detection
            # r.play(progress_bar=True)

            # region's metadata can also be used with the `save` method
            # (no need to explicitly specify region's object and `format` arguments)
            filename = r.save("region_{meta.start:.3f}-{meta.end:.3f}.wav")
            print("region saved as: {}".format(filename))

