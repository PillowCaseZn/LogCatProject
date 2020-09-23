#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author      : PillowCase
# Create Time : 2020/3/18  14:02
# Description :
import imp
import importlib
import platform
import re
import sys

from Scripts import LoggerUtils


def get_full_path(path):
    try:
        path = path.replace('\\', '/')
        path = re.sub('/+', '/', path)
        return path
    except Exception as e:
        LoggerUtils.error(e)


def get_python_version():
    # 获取当前Python版本
    version_info = sys.version_info
    major = version_info.major
    minor = version_info.minor
    micro = version_info.micro
    return "%s.%s.%s" % (major, minor, micro)


def get_system_type():
    """
    :return:系统类型
    """
    system = platform.system()
    # LoggerUtils.debug('System : %s' % system)
    if system == "Windows":
        system_os = "Windows"
    else:
        system_os = "Mac"
    return system_os


def change_default_encoding():
    # 修改默认的编码格式
    try:
        LoggerUtils.info('Change Default Encoding')
        # 判断Python版本
        version = get_python_version()
        LoggerUtils.info('Python Version : %s' % version)
        if version.startswith('2'):
            imp.reload(sys)
            # reload(sys)
            sys.setdefaultencoding('GB2312')
        elif version.startswith('3'):
            importlib.reload(sys)
    except Exception as e:
        LoggerUtils.error(e)
