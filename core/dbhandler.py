# -*- coding: utf-8 -*-
from db import redisClient
from core.proxy import Proxy
from config.configuration import default_config as config


class DBHandler(object):
    """
    通过redis进行ip proxy的增删改查
    对redis中存储的ip proxy pool的hash数据结构操作封装
    """

    def __init__(self):
        self.conf = config
        self.db = redisClient.new_client(self.conf.dbConn)
        # hash表名称
        self.db.checkoutTable(self.conf.tableName)

    def get(self, ptype=None):
        """
        return a proxy:
        """
        proxy = self.db.get(ptype)
        return Proxy.createFromJson(proxy) if proxy else None

    def pop(self, ptype):
        """
        return and delete a useful proxy
        :return:
        """
        proxy = self.db.pop(ptype)
        if proxy:
            return Proxy.createFromJson(proxy)
        return None

    def put(self, ptype):
        """
        put proxy into use proxy
        :return:
        """
        self.db.put(ptype)

    def update(self, proxy):
        """
        put proxy into use proxy
        :return:
        """
        self.db.update(proxy)

    def delete(self, proxy):
        """
        delete useful proxy
        :param proxy:
        :return:
        """
        return self.db.delete(proxy.proxy)

    def getAll(self, ptype=None):
        """
        get all proxy from pool as Proxy list
        :return:
        """
        proxies = self.db.getAll(ptype)
        return [Proxy.createFromJson(proxy) for proxy in proxies]

    def exists(self, proxy):
        """
        check proxy exists
        :param proxy:
        :return:
        """
        return self.db.exists(proxy.proxy)

    def getCount(self):
        """
        return raw_proxy and use_proxy count
        :return:
        """
        total_use_proxy = self.db.getCount()
        return {'count': total_use_proxy}
