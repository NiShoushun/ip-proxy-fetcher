# -*- coding: utf-8 -*-
from db import redisClient
from core.proxy import Proxy
from config.configuration import default_config as config


class ProxyDBHandler(object):
    """
    通过redis进行ip proxy的增删改查
    对redis中存储的ip proxy pool的hash数据结构操作封装
    """

    def __init__(self):
        self.conf = config
        self.db = redisClient.new_client(self.conf.dbConn)
        # hash表名称
        self.db.checkoutTable(self.conf.tableName)

    def get(self, https=False):
        """
        return a proxy
        Args:
            https: True/False 是否使用https
        Returns:
        """
        proxy = self.db.get(https)
        return Proxy.createFromJson(proxy) if proxy else None

    def pop(self, https):
        """
        return and delete a useful proxy
        :return:
        """
        proxy = self.db.pop(https)
        if proxy:
            return Proxy.createFromJson(proxy)
        return None

    def put(self, proxy):
        """
        put proxy into use proxy
        :return:
        """
        self.db.put(proxy)

    def delete(self, proxy):
        """
        delete useful proxy
        :param proxy:
        :return:
        """
        return self.db.delete(proxy.proxy)

    def getAll(self, https=False):
        """
        get all proxy from pool as Proxy list
        :return:
        """
        proxies = self.db.getAll(https)
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
