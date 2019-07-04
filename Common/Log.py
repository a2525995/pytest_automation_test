# -*- coding: utf-8 -*-

import logging
import os
import time

# log_path是日志存放路径地址
get_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(os.path.dirname(get_path), "log")

# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path): os.mkdir(log_path)


class Log:
    def __init__(self, filename=""):
        # 文件的命名
        self.logname = os.path.join(log_path, "%s.%s.log" % (filename, time.strftime("%Y-%m-%d")))
        self.logger = logging.getLogger(self.logname)
        self.logger.setLevel(logging.DEBUG)
        # 日志输出格式
        self.DATE_FORMAT = "%Y/%d/%m %H:%M:%S%p"
        self.formatter = logging.Formatter("%(asctime)s %(name)-8s %(levelname)-8s %(message)s",
                                           datefmt=self.DATE_FORMAT)

    # 创建一个FileHandler，用于写到本地
    def add_file_handler(self):
        fh = logging.FileHandler(self.logname, "a", encoding='utf-8')  # 追加模式
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)
        return fh

    def add_console_handler(self):
        ch = logging.StreamHandler()
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)
        return ch

    def remove_handler(self, handler):
        self.logger.removeHandler(handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)


class LogService:
    info_log = Log("info")
    info_log.add_file_handler()
    info_log.add_console_handler()
    error_log = Log("error")
    error_log.add_file_handler()
    error_log.add_console_handler()

    @staticmethod
    def debug(message):
        LogService.info_log.debug(message)

    @staticmethod
    def info(message):
        LogService.info_log.info(message)

    @staticmethod
    def error(message):
        LogService.error_log.error(message)

#
# if __name__ == "__main__":
#     log = Log()
#     log.info("--测试开始--")
#     log.info("操作步骤1，2,3")
#     log.warning("--测试结束--")
