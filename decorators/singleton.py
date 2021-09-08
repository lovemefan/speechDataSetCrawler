#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 下午2:32
# @Author  : lovemefan
# @File    : singleton.py
import threading


lock = threading.Lock()
# instance container
instances = {}


def singleton(cls):
    """this is decorator to decorate class , make the class singleton(修饰器实现单例模式) """
    def get_instance(*args, **kwargs):
        cls_name = cls.__name__
        try:
            lock.acquire()
            if cls_name not in instances:
                instance = cls(*args, **kwargs)
                print(f"create {cls_name}")
                instances[cls_name] = instance
        finally:
            lock.release()

        return instances[cls_name]

    return get_instance

def get_all_instance():
    """return all instance in the container"""
    return instances