#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author      : PillowCase
# Create Time : 2020/3/18  14:04
# Description :

import os
import shutil

from Scripts import ConfigUtils
from Scripts import LoggerUtils


def create_file(path):
    result = True
    try:
        path = ConfigUtils.get_full_path('%s' % path)
        if os.path.exists(path):
            result = False
        else:
            with open(path, 'w', encoding='UTF-8') as f:
                f.close()
    except Exception as e:
        result = False
        LoggerUtils.error(e)
    return result


def create_folder(path):
    """
    创建文件夹
    :param path: 将要创建的文件夹目录
    :return: 返回创建成功与否结果
    """
    result = True
    try:
        path = ConfigUtils.get_full_path('%s' % path)
        if os.path.exists(path):
            result = False
        else:
            os.makedirs(path)
    except Exception as e:
        result = False
        LoggerUtils.error(e)
    return result


def delete_folder(path):
    """
    删除文件夹
    :param path: 要删除的文件夹路径
    :return: 返回是否删除成功
    """
    result = True
    try:
        path = ConfigUtils.get_full_path('%s' % path)
        if os.path.exists(path):
            shutil.rmtree(path)
        else:
            result = False
    except Exception as e:
        result = False
        LoggerUtils.error(e)
    return result


def shutil_copy_folder(source_folder, target_folder):
    """
    复制文件夹
    :param source_folder:需要复制的文件夹
    :param target_folder: 复制到的目录路径
    :return:
    """
    source_folder = ConfigUtils.get_full_path('%s' % source_folder)
    target_folder = ConfigUtils.get_full_path('%s' % target_folder)

    shutil.copytree(source_folder, target_folder)


def copy_file(source_file, target_file):
    """
    复制文件到指定文件夹下
    :param source_file 需要复制的文件名路径
    :param target_file 复制到的文件名路径
    :return:
    """
    source_file = ConfigUtils.get_full_path('%s' % source_file)
    target_file = ConfigUtils.get_full_path('%s' % target_file)

    if os.path.exists(source_file) and os.path.isfile(source_file):
        shutil.copyfile(source_file, target_file)


def delete_file(path):
    """
    删除文件
    :param path:将要删除的文件路径
    :return:
    """
    result = True
    try:
        path = ConfigUtils.get_full_path('%s' % path)
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            else:
                result = False
        else:
            result = False
    except Exception as e:
        result = False
        LoggerUtils.error(e)
    return result


# 获取目录下所有文件列表
def list_files_in_folder(path, target_list, ignore_path_list):
    if os.path.exists(path):
        if os.path.isfile(path) and path not in ignore_path_list:
            target_list.append(path)
        elif os.path.isdir(path):
            for f in os.listdir(path):
                if path not in ignore_path_list:
                    list_files_in_folder(ConfigUtils.get_full_path("%s/%s" % (path, f)), target_list, ignore_path_list)
    return target_list
