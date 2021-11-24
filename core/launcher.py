# -*- coding: utf-8 -*-
import sys
from db import redisClient
from util import color
from util.logging import Logger
from config.configuration import default_config as config

log = Logger('launcher', level=config.log_level, file=config.log_to_file, color=color.YELLOW)


def startServer():
    __beforeStart()
    from api.proxyApi import start_server
    start_server()


def startScheduler():
    __beforeStart()
    from core.scheduler import runScheduler
    runScheduler()


def __beforeStart():
    print_version()
    print_config()
    if __checkDBConfig():
        log.info('exit!')
        sys.exit()


def print_version():
    log.info("ProxyPool Version: %s" % 1)


def print_config():
    conf = config
    log.info("ProxyPool configure HOST: %s" % conf.serverHost)
    log.info("ProxyPool configure PORT: %s" % conf.serverPort)
    log.info("ProxyPool configure DB_CONN: %s" % conf.dbConn)
    log.info("ProxyPool configure PROXY_FETCHER: %s" % conf.fetch_funcs)


def __checkDBConfig():
    conf = config
    db = redisClient.new_client(conf.dbConn)
    log.info("============ DATABASE CONFIGURE ================")
    log.info("DB_HOST: %s" % db.host)
    log.info("DB_PORT: %s" % db.port)
    log.info("DB_USER: %s" % db.username)
    log.info("=================================================")
    return db.test()
