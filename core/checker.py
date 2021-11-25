# -*- coding: utf-8 -*-


import queue
from threading import Thread
from datetime import datetime

from core.validator import ProxyValidator
from core.DB_handle import ProxyDBHandler
from util.logging import Logger
from config.configuration import default_config as config
from util import color


class IpProxyFilter(object):
    """ 执行校验 """

    @classmethod
    def validate(cls, proxy):
        """
        校验入口
        Args:
            proxy: Proxy Object
        Returns:
            Proxy Object
        """
        # 按照http方式检验，如果不通过再按照https方式检验
        if proxy.type.lower() == "sock4":
            # todo 校验sock类型代理
            return proxy
        http_r = cls.httpValidate(proxy)
        https_r = False if not http_r else cls.httpsValidate(proxy)

        # 设置该代理的检查次数以及最后一次的检查时间
        proxy.check_count += 1
        proxy.last_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        proxy.last_status = True if http_r else False
        if http_r:
            if proxy.fail_count > 0:
                proxy.fail_count -= 1
            proxy.https = True if https_r else False
        else:
            proxy.fail_count += 1
        return proxy

    @classmethod
    def httpValidate(cls, proxy):
        """调用http_validators列表中的方法，保留全部通过的proxy"""
        for func in ProxyValidator.http_validators:
            if not func(proxy.proxy):
                return False
        return True

    @classmethod
    def httpsValidate(cls, proxy):
        """调用https_validators列表中的方法，保留全部通过的proxy"""
        for func in ProxyValidator.https_validators:
            if not func(proxy.proxy):
                return False
        return True

    @classmethod
    def preValidate(cls, proxy):
        """调用pre_validators列表中的方法，保留全部通过的proxy"""
        for func in ProxyValidator.pre_validators:
            if not func(proxy):
                return False
        return True


class _ThreadChecker(Thread):
    """ 多线程检测 """

    def __init__(self, work_type, target_queue, thread_name):
        Thread.__init__(self, name=thread_name)
        self.work_type = work_type
        self.log = Logger("checker", level=config.log_level, file=config.log_to_file, color=color.GREEN)
        self.proxy_handler = ProxyDBHandler()
        self.target_queue = target_queue
        self.conf = config

    def run(self):
        self.log.info("{}ProxyCheck - {}: start".format(self.work_type.title(), self.name))
        while True:
            try:
                proxy = self.target_queue.get(block=True)
            except queue.Empty:
                self.log.info("{}ProxyCheck - {}: complete".format(self.work_type.title(), self.name))
                break
            # 检验proxy
            proxy = IpProxyFilter.validate(proxy)
            if self.work_type == "raw":
                self.__ifRaw(proxy)
            else:
                self.__ifUse(proxy)
            self.target_queue.task_done()

    def __ifRaw(self, proxy):
        """
        在抓取时，存入检查通过的代理
        """
        if proxy.last_status:
            if self.proxy_handler.exists(proxy):
                self.log.info('RawProxyCheck - {}: {} {}'.format(self.name, proxy.proxy.ljust(23), color.red('aleady in DB')))
            else:
                self.log.info(
                    'RawProxyCheck - {}: {} {}'.format(self.name, proxy.proxy.ljust(23), color.yellow('pass')))
                self.proxy_handler.put(proxy)
        else:
            self.log.info('RawProxyCheck - {}: {} {}'.format(self.name, proxy.proxy.ljust(23), color.red('fail')))

    def __ifUse(self, proxy):
        """
        通过检查结果，更新代理
        """
        if proxy.last_status:
            self.log.info(
                'UseProxyCheck - {}: {} {}'.format(self.name, proxy.proxy.ljust(23), color.yellow('recheck pass')))
            self.proxy_handler.update(proxy)
        else:
            #
            if proxy.fail_count > self.conf.maxFailCount:
                self.log.info('UseProxyCheck - {}: {} fail, count {} delete'.format(self.name,
                                                                                    proxy.proxy.ljust(23),
                                                                                    proxy.fail_count))
                self.proxy_handler.delete(proxy)
            else:
                self.log.info('UseProxyCheck - {}: {} fail, count {} keep'.format(self.name,
                                                                                  proxy.proxy.ljust(23),
                                                                                  proxy.fail_count))
                self.proxy_handler.update(proxy)


def Checker(tp, queue):
    """
    run Proxy ThreadChecker
    :param tp: raw/use
    :param queue: Proxy Queue
    :return:
    """
    thread_list = list()
    for index in range(config.check_thread_num):
        thread_list.append(_ThreadChecker(tp, queue, "thread_%s" % str(index).zfill(2)))

    for thread in thread_list:
        thread.setDaemon(True)
        thread.start()

    for thread in thread_list:
        thread.join()
