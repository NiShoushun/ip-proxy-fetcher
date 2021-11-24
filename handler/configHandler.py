# -*- coding: utf-8 -*-

import setting

from util.lazyProperty import LazyProperty


class ConfigHandler:

    def __init__(self):
        pass

    @LazyProperty
    def serverHost(self):
        return setting.HOST

    @LazyProperty
    def serverPort(self):
        return setting.PORT

    @LazyProperty
    def dbConn(self):
        return setting.DB_CONN

    @LazyProperty
    def tableName(self):
        return setting.TABLE_NAME

    @property
    def fetch_funcs(self):
        return setting.PROXY_FETCHER

    @LazyProperty
    def httpUrl(self):
        return setting.HTTP_URL

    @LazyProperty
    def httpsUrl(self):
        return setting.HTTPS_URL

    @LazyProperty
    def verifyTimeout(self):
        return int(setting.VERIFY_TIMEOUT)

    # @LazyProperty
    # def proxyCheckCount(self):
    #     return int(os.getenv("PROXY_CHECK_COUNT", setting.PROXY_CHECK_COUNT))

    @LazyProperty
    def maxFailCount(self):
        return int(setting.MAX_FAIL_COUNT)

    # @LazyProperty
    # def maxFailRate(self):
    #     return int(os.getenv("MAX_FAIL_RATE", setting.MAX_FAIL_RATE))

    @LazyProperty
    def poolSizeMin(self):
        return int(setting.POOL_SIZE_MIN)

    @LazyProperty
    def timezone(self):
        return setting.TIMEZONE


USER_CONFIG = ConfigHandler()
