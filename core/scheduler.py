# -*- coding: utf-8 -*-
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

from queue import Queue
from core.fetcher import Fetcher
from core.filter import Checker
from core.DB_handle import ProxyDBHandler
from util import color
from util.logging import Logger
from config.configuration import default_config as config




def __runProxyFetch():
    proxy_fetcher = Fetcher()
    cached_proxy_queue = Queue(maxsize=config.max_cached_proxy)
    for proxy in proxy_fetcher.run():
        cached_proxy_queue.put(proxy)
    Checker('raw', cached_proxy_queue)


def __runProxyCheck():
    proxy_handler = ProxyDBHandler()
    proxy_queue = Queue()
    if proxy_handler.db.getCount().get("total", 0) < proxy_handler.conf.poolSizeMin:
        __runProxyFetch()
    for proxy in proxy_handler.getAll():
        proxy_queue.put(proxy)
    Checker('use', proxy_queue)


def runScheduler():
    """
    启动调度器，两个任务：
    1. ip 代理抓取
    2. 检查已抓取的ip是否可用
    """
    __runProxyFetch()

    timezone = config.timezone
    scheduler_log = Logger("scheduler", color=color.BLUE, file=config.log_to_file, level=logging.INFO)
    scheduler = BlockingScheduler(logger=scheduler_log, timezone=timezone)

    scheduler.add_job(__runProxyFetch, 'interval', minutes=4, id="proxy_fetch", name="proxy采集")
    scheduler.add_job(__runProxyCheck, 'interval', minutes=2, id="proxy_check", name="proxy检查")
    executors = {
        'default': {'type': 'threadpool', 'max_workers': config.fetch_thread_num},
        'processpool': ProcessPoolExecutor(max_workers=config.process_pool_max_worker)
    }

    job_defaults = {
        'coalesce': False,
        'max_instances': 10
    }

    scheduler.configure(executors=executors, job_defaults=job_defaults, timezone=timezone)

    scheduler.start()


if __name__ == '__main__':
    runScheduler()
