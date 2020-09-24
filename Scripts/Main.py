#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author      : PillowCase
# Create Time : 2020-09-23 14:34
# Description : 
import json
import os
import re
import subprocess
import time

from Scripts import ConfigUtils
from Scripts import LoggerUtils
from Scripts import PathManager


def get_package_pid(item):
    try:
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

        return {
            'PackageName': item['PackageName'],
            'Pid': pid,
        }
    except Exception as e:
        LoggerUtils.error(e)


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
                            package_list.append(get_package_pid(item))
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
                if package_list is not None and isinstance(package_list, list) and len(package_list) > 0:
                    for item in package_list:
                        dealing_log_message(item)
                        if item['Pid'] == '0' or item['Pid'] == 0:
                            item = get_package_pid(item)
                        dealing_log_message(item)

                        if item['Pid'] == '0' or item['Pid'] == 0:
                            continue

                        report_file_path = ConfigUtils.get_full_path('%s/report-%s-%s.txt'
                                                                     % (PathManager.report_folder_path(),
                                                                        item['PackageName'], time.strftime('%Y%m%d')))
                        # 1、拆分LogCat
                        logcat_data = []
                        with open(output_file_path, 'r', encoding='UTF-8') as f:
                            for line in f.readlines():
                                if re.match('\\b[0-9]{2}.*%s.*(([0-9]{3})|([0-9]{4})|([0-9]{5}))\\s.*' % item['Pid'],
                                            line):
                                    logcat_data.append(line)
                        # 2、设备信息  系统版本、SDK版本、型号、品牌
                        cmd_list = [
                            {
                                'name': '系统版本',
                                'cmd': 'ro.build.version.release'
                            },
                            {
                                'name': 'SDK版本',
                                'cmd': 'ro.build.version.sdk',
                            },
                            {
                                'name': '型号',
                                'cmd': 'o.product.model',
                            },
                            {
                                'name': '品牌',
                                'cmd': 'o.product.brand'
                            },
                        ]
                        device_info = []
                        for item in cmd_list:
                            cmd = '%s -s %s shell "getprop %s"' % (adb_file_path, device['Name'], item['cmd'])
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
                            device_info.append({
                                'name': item['name'],
                                'result': str.strip(result_log)
                            })

                        # 3、数据分析
                        with open(report_file_path, 'w', encoding='UTF-8')as f:
                            f.write('==========>     报告时间     <==========\n%s\n' % time.strftime('%Y-%m-%d %H:%M:%S'))
                            # f.write('==========>     接口测试报告     <==========\n')
                            f.write('==========>     设备信息     <==========\n')
                            for item in device_info:
                                f.write(item['name'] + ' : ' + item['result'] + '\n')

                            f.write('==========>     LogCat 日志     <==========\n')
                            for item in logcat_data:
                                f.write(item)
                            f.close()
