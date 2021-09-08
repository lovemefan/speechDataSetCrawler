# -*- coding: utf-8 -*-
# @Time  : 2021/3/14 16:53
# @Author : lovemefan
# @File : sqliteHelper.py
import logging
import sqlite3
import os
import sys
import threading

from config.BaseConfig import BaseConfig
from config.Config import Config
from utils.log import logger

lock = threading.Lock()
root_dir = Config.get_instance().get('file.root_path')


class SqliteHelper(BaseConfig):
    def __init__(self):
        db_file_path = os.path.join(root_dir, 'audio.sqlite')

        # get connection,if not exist then create
        self.conn = sqlite3.connect(db_file_path)
        cur = self.conn.cursor()
        cur.execute("select name from sqlite_master where type='table' order by name")
        self.conn.commit()
        tables = cur.fetchall()

        # create tables
        if len(tables) == 0:
            # create db base with sql file
            with open(os.path.join(root_dir, 'createDB.sql'), 'r', encoding='utf-8') as f:
                create_sql = f.read()
                cur.executescript(create_sql)

        self.conn.commit()
        cur.close()

    def execute(self, fn):
        """use the decorator to auto execute sql
        Args:
            fn the function
        Returns:
            tuple the results
        """
        def wrapped(*args, **kwargs):
            lock.acquire()
            cur = self.conn.cursor()
            sql = fn(*args, **kwargs)
            logger.info(f"Executing: {sql}")
            cur.execute(sql)
            self.conn.commit()
            result = cur.fetchall()
            cur.close()
            lock.release()
            logger.info(f"Execution finished")

            return result
        return wrapped

    def execute_sql(self, sql):
        """use the decorator to execute sql
        Args:
            fn the function
        Returns:
            tuple the results
        """
        def decorator(fn):
            def wrapped(*args, **kwargs):
                logger.info(f"Executing: {sql}")
                lock.acquire()
                cur = self.conn.cursor()
                cur.execute(sql)
                self.conn.commit()
                result = cur.fetchall()
                cur.close()
                lock.release()
                logger.info(f"Execution finished")
                return fn(*args, **kwargs, result=result)
            return wrapped
        return decorator

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    sql = SqliteHelper()