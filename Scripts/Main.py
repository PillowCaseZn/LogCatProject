#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author      : PillowCase
# Create Time : 2020-09-23 14:34
# Description : 
import json
import os
import subprocess
import time

from Scripts import ConfigUtils
from Scripts import LoggerUtils
from Scripts import PathManager


def dealing_log_message(message):
    try:
        if message is not None and isinstance(message, bytes):
            message = bytes.decode(message, encoding='GB2312')
            if message == '':
                message = None

        if message is not None and message != '':
            LoggerUtils.debug(
                '==========> Start Message <==========\n'
                '%s\n'
                '==========> End Message <==========\n'
                % message
            )

        return message
    except Exception as e:
        LoggerUtils.error(e)


LoggerUtils.init()
ConfigUtils.change_default_encoding()

adb_file_path = ConfigUtils.get_full_path('%s/adb' % PathManager.tools_folder_path())

cmd = '%s devices' % adb_file_path
dealing_log_message(cmd)
process = subprocess.Popen(cmd,
                           shell=True,
                           stdin=None,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE
                           )
result_log, error_log = process.communicate()
result_log = dealing_log_message(result_log)
error_log = dealing_log_message(error_log)

if result_log is not None:
    # 处理返回的字段
    device_file_path = ConfigUtils.get_full_path('%s/devices-%s.txt'
                                                 % (PathManager.devices_folder_path(), time.strftime('%Y%m%d')))
    device_data = []
    with open(device_file_path, 'w', encoding='UTF-8') as f:
        for line in result_log.split('\n'):
            if line != '':
                if not line.startswith('List'):
                    device_data.append(line)
                f.write(line + '\n')
        f.close()

    # LoggerUtils.info(device_data)

    if device_data is not None and len(device_data) > 0:
        device_list = []
        for item in device_data:
            name, status = item.split()
            # LoggerUtils.debug('name : %s\nstatus:%s' % (name, status))
            device_list.append({
                'Name': name,
                'Status': status
            })

        # LoggerUtils.info('Device List : %s' % device_list)

        if device_list is not None:
            device = None
            if len(device_list) == 1:
                device = device_list[0]

            if device is not None \
                    and 'Name' in device \
                    and 'Status' in device \
                    and device['Status'] == 'device':
                LoggerUtils.info('Connecting Device %s .....' % device['Name'])

                # 获取需要单独打出报告的应用PID
                package_list = []
                package_config_file_path = ConfigUtils.get_full_path(
                    '%s/PackageConfig.json' % PathManager.get_root_path())
                if os.path.exists(package_config_file_path):
                    with open(package_config_file_path, 'r', encoding='UTF-8') as f:
                        data = json.load(f)
                        f.close()

                        for item in data:
                            cmd = '%s -s %s shell "ps | grep %s"' % (adb_file_path, device['Name'], item['PackageName'])
                            dealing_log_message(cmd)
                            output_file_path = ConfigUtils.get_full_path('%s/%s-%s-%s.log' %
                                                                         (PathManager.devices_folder_path(),
                                                                          device['Name'],
                                                                          item['PackageName'],
                                                                          time.strftime('%Y%m%d')))

                            process = subprocess.Popen(cmd,
                                                       shell=True,
                                                       stdin=None,
                                                       stdout=subprocess.PIPE,
                                                       stderr=subprocess.PIPE
                                                       )
                            result_log, error_log = process.communicate()
                            result_log = dealing_log_message(result_log)
                            error_log = dealing_log_message(error_log)

                            pid = 0
                            if result_log is not None and len(result_log) > 0:
                                with open(output_file_path, 'w', encoding='UTF-8') as f:
                                    f.write(result_log)
                                    f.close()

                                pid = result_log.split()[1]

                            package_list.append({
                                'PackageName': item['PackageName'],
                                'Pid': pid,
                            })
                dealing_log_message(package_list)

                # 连接设备，捕获日志
                cmd = '%s -s %s logcat -v threadtime' % (adb_file_path, device['Name'])
                dealing_log_message(cmd)
                output_file_path = ConfigUtils.get_full_path('%s/%s-%s.log' %
                                                             (PathManager.logcat_folder_path(), device['Name'],
                                                              time.strftime('%Y%m%d')))
                channel_output_file = open(output_file_path, 'w', encoding='UTF-8')
                error_file_path = ConfigUtils.get_full_path('%s/%s-%s.log' %
                                                            (PathManager.logcat_error_folder_path(), device['Name'],
                                                             time.strftime('%Y%m%d')))
                channel_error_file = open(error_file_path, 'w', encoding='UTF-8')

                process = subprocess.Popen(cmd,
                                           shell=True,
                                           stdin=None,
                                           stdout=channel_output_file,
                                           stderr=channel_error_file
                                           )

                LoggerUtils.info('Start Catching Device Logact Message ...')
                input_reuslt = input('Press \'X\' to Stop Catching Device LogCat\n')
                while input_reuslt != 'X' and input_reuslt != 'x':
                    input_reuslt = input('Press \'X\' to Stop Catching Device LogCat\n')
                else:
                    if input_reuslt is not None \
                            and (input_reuslt == 'X' or input_reuslt == 'x'):
                        LoggerUtils.info('Stop Catching Device Logact Message ...')
                        process.terminate()
                        process.kill()

                        if channel_output_file is not None:
                            channel_output_file.close()
                        if channel_error_file is not None:
                            channel_error_file.close()

                # 判断是否需要Report
                # 1、拆分LogCat
                # 2、设备信息
                # 3、数据分析