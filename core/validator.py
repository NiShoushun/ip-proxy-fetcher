# -*- coding: utf-8 -*-

"""
ip 检验方法定义
"""

from re import findall
from requests import head

from config.configuration import default_config as config


HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
          'Accept': '*/*',
          'Connection': 'keep-alive',
          'Accept-Language': 'zh-CN,zh;q=0.8'}


class ProxyValidator:
    pre_validators = []
    http_validators = []
    https_validators = []

    @classmethod
    def addPreValidator(cls, func):
        cls.pre_validators.append(func)
        return func

    @classmethod
    def addHttpValidator(cls, func):
        cls.http_validators.append(func)
        return func

    @classmethod
    def addHttpsValidator(cls, func):
        """预先检验ip格式，"""
        cls.https_validators.append(func)
        return func


@ProxyValidator.addPreValidator
def formatValidator(proxy):
    """检查代理格式"""
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


@ProxyValidator.addHttpValidator
def httpTimeOutValidator(proxy):
    """ http检测超时 """

    proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
    try:
        r = head(config.httpUrl, headers=HEADER, proxies=proxies, timeout=config.verifyTimeout)
        return True if r.status_code == 200 else False
    except Exception as e:
        return False


@ProxyValidator.addHttpsValidator
def httpsTimeOutValidator(proxy):
    """https检测超时"""
    proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
    try:
        r = head(config.httpsUrl, headers=HEADER, proxies=proxies, timeout=config.verifyTimeout, verify=False)
        return True if r.status_code == 200 else False
    except Exception as e:
        return False

