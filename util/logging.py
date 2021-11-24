# -*- coding: utf-8 -*-

import logging
import os
import platform
from logging.handlers import TimedRotatingFileHandler
from util import color as colorutil
from config.configuration import default_config as config

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')

if not os.path.exists(LOG_PATH):
    try:
        os.mkdir(LOG_PATH)
    except FileExistsError:
        pass


class Logger(logging.Logger):
    """
    LogHandler
    """

    def __init__(self, name, color=colorutil.normal, level=logging.DEBUG, stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        # 彩色打印输出流
        self.color = color
        if stream:
            self.__addStreamHandler()
        if file:
            if platform.system() != "Windows":
                self.__addFileHandler()

    def __addFileHandler(self):
        """
        文件类型日志
        :return:
        """
        file_name = os.path.join(LOG_PATH, '{name}.log'.format(name=self.name))
        # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=15)
        file_handler.suffix = '%Y%m%d.log'
        file_handler.setLevel(self.level)
        formatter = logging.Formatter(config.logfile_format)
        file_handler.setFormatter(formatter)

        self.file_handler = file_handler
        self.addHandler(file_handler)

    def __addStreamHandler(self):
        """
        输出流类型日志
        :return:
        """
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            colorutil.color_str(self.color, config.log_format))
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(self.level)
        self.addHandler(stream_handler)
