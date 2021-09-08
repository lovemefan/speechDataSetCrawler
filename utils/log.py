# -*- coding: utf-8 -*-
# @Time  : 2021/3/16 14:42
# @Author : lovemefan
# @File : log.py
import logging
import os

from config.Config import Config

root_dir = Config.get_instance().get('file.root_path')
# root_dir = os.path.dirname(os.getcwd())
print(root_dir)
logger = logging.getLogger('audio')

error_handler = logging.FileHandler(os.path.join(root_dir, 'log/sqlite/sqlite_error.log'))
error_handler.setLevel(logging.WARN)
error_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

all_handler = logging.FileHandler(os.path.join(root_dir, 'log/sqlite/sqlite_all.log'))
all_handler.setLevel(logging.INFO)
all_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

logger.addHandler(error_handler)
logger.addHandler(all_handler)
logger.addHandler(console)
