# -*- coding: utf-8 -*-
import logging
from pprint import pprint

from util.lazyProperty import LazyProperty
import json

DEFAULT_CFG_PATH = 'setting.json'


class Configuration:

    def __init__(self, cfg_dict: dict):
        self.__cfg = cfg_dict

    @LazyProperty
    def serverHost(self):
        return self.__cfg.get('host', "0.0.0.0")

    @LazyProperty
    def serverPort(self):
        return self.__cfg.get('port', "6379")

    @LazyProperty
    def dbConn(self):
        return self.__cfg.get('connect', 'redis://@127.0.0.1:6379/0')

    @LazyProperty
    def tableName(self):
        return self.__cfg.get('table_name', 'default_pool')

    @property
    def fetch_funcs(self):
        return self.__cfg.get('proxy_src', [
            "freeProxy01",
            "freeProxy02",
            "freeProxy03",
            "freeProxy04",
            "freeProxy05",
            "freeProxy06",
            "freeProxy07",
            "freeProxy08",
            "freeProxy09",
            "freeProxy10",
        ], )

    @LazyProperty
    def httpUrl(self):
        return self.__cfg.get('http_test_url', "http://httpbin.org")

    @LazyProperty
    def httpsUrl(self):
        return self.__cfg.get('https_test_url', "https://httpbin.org")

    @LazyProperty
    def verifyTimeout(self):
        return self.__cfg.get('verify_timeout', 10)

    # @LazyProperty
    # def proxyCheckCount(self):
    #     return int(os.getenv("PROXY_CHECK_COUNT", setting.PROXY_CHECK_COUNT))

    @LazyProperty
    def maxFailCount(self):
        return self.__cfg.get("max_fail_count", 0)

    # @LazyProperty
    # def maxFailRate(self):
    #     return int(os.getenv("MAX_FAIL_RATE", setting.MAX_FAIL_RATE))

    @LazyProperty
    def poolSizeMin(self):
        return self.__cfg.get("pool_size_min", 20)

    @LazyProperty
    def timezone(self):
        return self.__cfg.get("time_zone", "Asia/Shanghai")

    @LazyProperty
    def log_format(self):
        return self.__cfg.get("log_format", "%(asctime)s %(filename)s[line:] %(levelname)s %(message)s")

    @LazyProperty
    def logfile_format(self):
        return self.__cfg.get("logfile_format", "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")

    @LazyProperty
    def log_level(self):
        log_level = self.__cfg.get("log_level", "INFO")
        return getattr(logging, log_level)

    @LazyProperty
    def log_to_file(self):
        return self.__cfg.get("log_to_file", True)

    @LazyProperty
    def check_thread_num(self):
        return self.__cfg.get("check_thread_num", 20)

    @LazyProperty
    def fetch_thread_num(self):
        return self.__cfg.get("fetch_thread_num", 20)

    @LazyProperty
    def process_pool_max_worker(self):
        return self.__cfg.get("process_pool_max_worker", 5)

    @LazyProperty
    def max_cached_proxy(self):
        return self.__cfg.get("max_cached_proxy_size", 1000)



    @LazyProperty
    def fetch_job_interval(self):
        return self.__cfg.get("fetch_job_interval", 2*60)

    @LazyProperty
    def check_job_interval(self):
        return self.__cfg.get("check_job_interval", 3*60)


def print_config(self):
    pprint(self.__cfg)


def load_config(cfg_json):
    """
    从json文件中读取配置文件，生成Configuration对象
    """
    try:

        with open('setting.json', 'br') as setting_file:
            cfg_dict = json.load(setting_file)
            return Configuration(cfg_dict)
    except FileNotFoundError as e:
        print("can't find setting.json")
        raise e


# 加载配置
default_config = load_config(DEFAULT_CFG_PATH)

if __name__ == "__main__":
    level = getattr(logging, "INFO")
    print(level)
