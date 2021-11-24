# -*- coding: utf-8 -*-


from threading import Thread
from core.proxy import Proxy
from core.filter import IpProxyFilter
from handler.logHandler import LogHandler
from handler.proxyHandler import ProxyHandler
from proxyfetchermodule import proxy_fetcher_module
from handler import configHandler
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
        self.fetch_func = getattr(proxy_fetcher_module, fetch_source, None)
        self.log = LogHandler("fetcher", color=color.CYAN)
        self.conf = configHandler.USER_CONFIG
        self.proxy_handler = ProxyHandler()

    def run(self):
        self.log.info("ProxyFetch - {func}: start".format(func=self.fetch_source))
        try:
            for proxy in self.fetch_func():
                self.log.info('ProxyFetch - %s: %s get' % (self.fetch_source, proxy.ljust(23)))
                proxy = proxy.strip()
                if proxy in self.proxy_dict:
                    self.proxy_dict[proxy].add_source(str(self.fetch_source))
                else:
                    self.proxy_dict[proxy] = Proxy(
                        proxy, source=self.fetch_source)
        except Exception as e:
            self.log.error("ProxyFetch - {func}: error".format(func=self.fetch_source))
            self.log.error(str(e))


class Fetcher(object):
    name = "fetcher"

    def __init__(self):
        self.log = LogHandler(self.name,color.WHITE)
        self.conf = configHandler.USER_CONFIG

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
            fetcher = getattr(proxy_fetcher_module, fetch_func, None)
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
