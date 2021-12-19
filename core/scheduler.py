# -*- coding: utf-8 -*-
import threading

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

from queue import Queue
from core.fetcher import Fetcher
from core.checker import Checker
from core.dbhandler import DBHandler
from util import color
from util.logging import Logger
from config.configuration import default_config as config


def fetchProxy():
    """
    抓取并检查ip proxy
    """
    cached_proxy_queue = Queue(maxsize=config.max_cached_proxy)

    def check():
        Checker('raw', cached_proxy_queue)

    checkJob = threading.Thread(target=check)
    checkJob.setDaemon(True)
    checkJob.start()
    proxy_fetcher = Fetcher()

    for proxy in proxy_fetcher.run():
        cached_proxy_queue.put(proxy)


def checkProxy():
    """
    检查数据库已有ip proxy
    """
    proxy_handler = DBHandler()
    proxy_queue = Queue()
    # 如果数据库中的数据量过小，则进行抓取活动
    if proxy_handler.db.getCount().get("total", 0) < proxy_handler.conf.poolSizeMin:
        fetchProxy()
    # 从数据库中取出ip proxy 再次就你行检验
    for proxy in proxy_handler.getAll():
        proxy_queue.put(proxy)
    Checker('use', proxy_queue)


def start():
    """
    启动调度器，两个任务：
    1. ip 代理抓取
    2. 检查已抓取的ip是否可用
    """
    threading.Thread(target=fetchProxy).start()

    timezone = config.timezone
    scheduler_log = Logger("scheduler", color=color.BLUE, file=config.log_to_file, level=config.log_level)
    scheduler = BlockingScheduler(logger=scheduler_log, timezone=timezone)

    scheduler.add_job(fetchProxy, 'interval', seconds=config.fetch_job_interval, id="proxy_fetch", name="proxy采集")
    scheduler.add_job(checkProxy, 'interval', seconds=config.check_job_interval, id="proxy_check", name="proxy检查")
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
    start()
