#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author      : PillowCase
# Create Time : 2020-04-21 14:28
# Description : 各种路径配置、读取

import os

from Scripts import ConfigUtils
from Scripts import FileUtils


def get_root_path():
    """
    :return: 获取根目录路径
    """
    path = ConfigUtils.get_full_path('%s' % os.path.abspath(os.getcwd()))
    return path


def logger_folder_path():
    path = ConfigUtils.get_full_path('%s/Logger' % get_root_path())
    if os.path.exists(path) is False:
        FileUtils.create_folder(path)
    return path


def logcat_folder_path():
    path = ConfigUtils.get_full_path('%s/LogCat' % get_root_path())
    if os.path.exists(path) is False:
        FileUtils.create_folder(path)
    return path


def logcat_error_folder_path():
    path = ConfigUtils.get_full_path('%s/LogCatError' % get_root_path())
    if os.path.exists(path) is False:
        FileUtils.create_folder(path)
    return path


def scripts_folder_path():
    path = ConfigUtils.get_full_path('%s/Scripts' % get_root_path())
    return path


def tools_folder_path():
    path = ConfigUtils.get_full_path('%s/Tools' % get_root_path())
    return path


def devices_folder_path():
    path = ConfigUtils.get_full_path('%s/Devices' % get_root_path())
    if os.path.exists(path) is False:
        FileUtils.create_folder(path)
    return path


def report_folder_path():
    path = ConfigUtils.get_full_path('%s/Report' % get_root_path())
    if os.path.exists(path) is False:
        FileUtils.create_folder(path)
    return path
