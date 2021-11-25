# -*- coding: utf-8 -*-


from threading import Thread

import proxy_src
from core.proxy import Proxy
from core.checker import IpProxyFilter
from util.logging import Logger
from core.DB_handle import ProxyDBHandler
from config.configuration import default_config as config
from util import color


class _ThreadFetcher(Thread):
    """
    通过开启线程运行proxyFetcher模块的抓取函数
    """

    def __init__(self, fetch_source, proxy_dict):
        Thread.__init__(self)
        self.fetch_source = fetch_source
        self.proxy_dict = proxy_dict
        # 从proxyFetcher模块中获取抓取函数
        self.fetch_func = getattr(proxy_src, fetch_source, None)
        self.log = Logger("fetcher", level=config.log_level, file=config.log_to_file, color=color.CYAN)
        self.conf = config
        self.proxy_handler = ProxyDBHandler()

    def run(self):
        self.log.info("ProxyFetch - {func}: start".format(func=self.fetch_source))
        try:
            for proxy, type, anonymous,region in self.fetch_func():
                self.log.info('fetch - %s get=> %s, %s, %s, %s' % (
                self.fetch_source, proxy, type, anonymous, region))
                proxy = proxy.strip()
                if proxy in self.proxy_dict:
                    self.proxy_dict[proxy].add_source(self.fetch_source)
                else:
                    self.proxy_dict[proxy] = Proxy(
                        proxy, source=self.fetch_source, anonymous=anonymous, type=type, region=region)
        except Exception as e:
            self.log.error("ProxyFetch - {func}: error".format(func=self.fetch_source))
            self.log.error(str(e))


class Fetcher(object):
    name = "fetcher"

    def __init__(self):
        self.log = Logger(self.name, level=config.log_level, color=color.WHITE)
        self.conf = config

    def run(self):
        """
        fetch proxy with proxyFetcher
        :return:
        """
        proxy_dict = dict()
        thread_list = list()
        self.log.info("ProxyFetch : start")

        # 读取config中定义的抓取方法，新建_ThreadFetcher对象，开启线程运行抓取函数
        for fetch_func in self.conf.fetch_funcs:
            self.log.info("ProxyFetch - {func}: start".format(func=fetch_func))
            fetcher = getattr(proxy_src, fetch_func, None)
            if not fetcher:
                self.log.error("ProxyFetch - {func}: class method not exists!".format(func=fetch_func))
                continue
            if not callable(fetcher):
                self.log.error("ProxyFetch - {func}: must be class method".format(func=fetch_func))
                continue
            thread_list.append(_ThreadFetcher(fetch_func, proxy_dict))

        # 开启线程列表中的线程
        for thread in thread_list:
            thread.setDaemon(True)
            thread.start()

        for thread in thread_list:
            thread.join()

        self.log.info("ProxyFetch - all complete!")

        for _ in proxy_dict.values():
            if IpProxyFilter.preValidate(_.proxy):
                yield _
