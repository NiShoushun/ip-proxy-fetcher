# -*- coding: utf-8 -*-


from requests.models import Response
from lxml import etree
import requests
import random
import time

from util.logging import Logger
from util import color
from config.configuration import default_config as config


class WebRequest(object):
    name = "web_request"

    def __init__(self, *args, **kwargs):
        self.log = Logger(self.name, color=color.RESET,level=config.log_level, file=False)
        self.response = Response()

    @property
    def user_agent(self):
        """
        返回1个随机代理
        :return:
        """
        ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        ]
        return random.choice(ua_list)

    @property
    def header(self):
        """
        返回 http head
        :return:
        """
        return {'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN,zh;q=0.8'}

    def get(self, url, header=None, retry_time=3, timeout=5, base_interval=1, *args, **kwargs):
        """
        get method
        :param url: target url
        :param header: headers
        :param retry_time: retry time
        :param base_interval: retry interval
        :param timeout: network timeout
        :return:
        """
        headers = self.header
        if header and isinstance(header, dict):
            headers.update(header)
        while True:
            try:
                self.response = requests.get(url, headers=headers, timeout=timeout, *args, **kwargs)
                return self
            except Exception as e:
                self.log.debug("requests: %s error: %s" % (url, str(e)))
                retry_time -= 1
                if retry_time <= 0:
                    return None
                self.log.debug("retry %s second after" % base_interval)
                base_interval += 2
                time.sleep(base_interval)

    @property
    def tree(self):
        """
        返回 html dom 树
        """
        return etree.HTML(self.response.content)

    @property
    def text(self):
        """
        返回响应内容
        """
        return self.response.text

    @property
    def json(self):
        """
        尝试对响应转化为json格式，并返回
        """
        try:
            return self.response.json()
        except Exception as e:
            self.log.error(str(e))
            return {}
