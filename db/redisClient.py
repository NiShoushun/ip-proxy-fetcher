# -*- coding: utf-8 -*-


from urllib import parse

from redis import exceptions
from redis.connection import BlockingConnectionPool
from util.logging import Logger
from config.configuration import default_config as config
from random import choice
from redis import Redis
import json

from util import color

DEFAULT_POOL_NAME = "ip_proxy_pool"


class RedisClient:
    """
    Redis client

    Redis中代理存放的结构为hash：
    key为ip:port, value为代理属性的字典;

    """

    def __init__(self, host, port, username, password, db, pool_name=None):
        """
        init redis client

        param pool_name: 存放ip proxy的hash map
        :return:
        """
        self.pool_name = DEFAULT_POOL_NAME if pool_name is None else pool_name
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db = db

        self.__conn = Redis(connection_pool=BlockingConnectionPool(decode_responses=True,
                                                                   timeout=5,
                                                                   socket_timeout=5,
                                                                   host=host,
                                                                   port=port,
                                                                   username=username,
                                                                   password=password,
                                                                   db=db,
                                                                   client_name=DEFAULT_POOL_NAME))

    def get(self, https):
        """
        返回一个代理
        :param https: 只使用https
        :return:
        """
        if https:
            items = self.__conn.hvals(self.pool_name)
            # 过滤出https类型的代理
            proxies = list(filter(lambda x: json.loads(x).get("https"), items))
            return choice(proxies) if proxies else None
        else:
            proxies = self.__conn.hkeys(self.pool_name)
            proxy = choice(proxies) if proxies else None
            return self.__conn.hget(self.pool_name, proxy) if proxy else None

    def put(self, proxy_obj):
        """
        将代理放入hash, 使用changeTable指定hash name
        :param proxy_obj: Proxy obj
        :return:
        """
        # 以proxy对象的proxy ip 作为key，全部信息的json格式数据作为value，存入 redis 中的hash map中
        data = self.__conn.hset(self.pool_name, proxy_obj.proxy, proxy_obj.to_json)
        return data

    def pop(self, https):
        """
        弹出一个代理
        :return: dict {proxy: value}
        """
        proxy = self.get(https)
        if proxy:
            self.__conn.hdel(self.pool_name, json.loads(proxy).get("proxy", ""))
        return proxy

    def delete(self, proxy_str):
        """
        移除指定代理
        :param proxy_str: proxy str
        :return:
        """
        return self.__conn.hdel(self.pool_name, proxy_str)

    def exists(self, proxy_str):
        """
        判断指定代理是否存在, 使用changeTable指定hash name
        :param proxy_str: proxy str
        :return:
        """
        return self.__conn.hexists(self.pool_name, proxy_str)

    def update(self, proxy_obj):
        """
        更新 proxy 属性
        :param proxy_obj:
        :return:
        """
        return self.__conn.hset(self.pool_name, proxy_obj.proxy, proxy_obj.to_json)

    def getAll(self, https):
        """
        字典形式返回所有代理, 使用changeTable指定hash name
        :return:
        """
        items = self.__conn.hvals(self.pool_name)
        if https:
            return list(filter(lambda x: json.loads(x).get("https"), items))
        else:
            return items

    def clear(self):
        """
        清空所有代理, 使用changeTable指定hash name
        :return:
        """
        return self.__conn.delete(self.pool_name)

    def getCount(self):
        """
        返回代理数量
        :return:
        """
        proxies = self.getAll(https=False)
        return {'total': len(proxies), 'https': len(list(filter(lambda x: json.loads(x).get("https"), proxies)))}

    def checkoutTable(self, name):
        """
        切换操作对象
        :param name:
        :return:
        """
        self.pool_name = name

    def test(self):
        log = Logger('redis_client', file=config.log_to_file, color=color.red)
        try:
            self.getCount()
        except exceptions.TimeoutError as e:
            log.error('redis connection time out: %s' % str(e), exc_info=True)
            return e
        except exceptions.ConnectionError as e:
            log.error('redis connection error: %s' % str(e), exc_info=True)
            return e
        except exceptions.ResponseError as e:
            log.error('redis connection error: %s' % str(e), exc_info=True)
            return e


def new_client(con):
    """return new redis client by connection url
    """
    db_conf = parse.urlparse(con)
    db_host = db_conf.hostname
    db_port = db_conf.port
    db_user = db_conf.username
    db_pwd = db_conf.password
    db_name = db_conf.path[1:]
    return RedisClient(
        host=db_host,
        port=db_port,
        username=db_user,
        password=db_pwd,
        db=db_name)
