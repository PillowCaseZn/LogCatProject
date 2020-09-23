#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author      : PillowCase
# Create Time : 2020/3/18  13:57
# Description :
import logging
import os
import time

from Scripts import ConfigUtils
from Scripts import FileUtils
from Scripts import PathManager

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)


def info(msg, *args):
    if len(msg) <= 0:
        return
    logger.info(u"%s" % msg, *args)


def debug(msg, *args):
    if len(msg) <= 0:
        return
    logger.debug(u"%s" % msg, *args)


def warning(msg, *args):
    if len(msg) <= 0:
        return
    logger.warning(u"%s" % msg, *args)


def error(msg, *args):
    logger.error(u"%s" % msg, *args)


def init():
    logger_folder_path = PathManager.logger_folder_path()
    logger_file_path = ConfigUtils.get_full_path(
        '%s/log_%s.log' % (logger_folder_path, time.strftime("%Y%m%d")))
    if os.path.exists(logger_file_path) is False:
        FileUtils.create_file(logger_file_path)
    formatter = logging.Formatter('%(asctime)s: %(message)s')

    if not logger.handlers:
        # 配置写入文件的拦截器
        file_handler = logging.FileHandler(logger_file_path, "w", "UTF-8")
        file_handler.setLevel(logging.DEBUG)
        # file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 配置输出到终端命令行的拦截器
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        # stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
