# -*- coding: utf-8 -*-

import json


class Proxy(object):
    """
    代理类，
    """

    def __init__(self, proxy, fail_count=0, region="", anonymous="",
                 source="", check_count=0, last_status="", last_time="", https=False, ptype=None):
        self._type = ptype
        self._proxy = proxy
        self._fail_count = fail_count
        self._region = region
        self._anonymous = anonymous
        self._source = source
        self._check_count = check_count
        self._last_status = last_status
        self._last_time = last_time
        self._https = https

    @classmethod
    def createFromJson(cls, proxy_json):
        """
        从json格式的代理中生成一个Proxy对象
        """
        _dict = json.loads(proxy_json)
        return Proxy(proxy=_dict.get("proxy", ""),
                     fail_count=_dict.get("fail_count", 0),
                     region=_dict.get("region", ""),
                     anonymous=_dict.get("anonymous", ""),
                     source=_dict.get("source", ""),
                     check_count=_dict.get("check_count", 0),
                     last_status=_dict.get("last_status", ""),
                     last_time=_dict.get("last_time", ""),
                     https=_dict.get("https", False),
                     ptype=_dict.get("type", "")
                     )

    @property
    def proxy(self) -> str:
        """ 代理 ip:port """
        return self._proxy

    @property
    def fail_count(self):
        """ 检测失败次数 """
        return self._fail_count

    @property
    def region(self):
        """ 地理位置(国家/城市) """
        return self._region

    @property
    def anonymous(self):
        """ 匿名 """
        return self._anonymous

    @property
    def source(self):
        """ 代理来源 """
        return self._source

    @property
    def check_count(self):
        """ 代理检测次数 """
        return self._check_count

    @property
    def last_status(self):
        """ 最后一次检测结果  True -> 可用; False -> 不可用"""
        return self._last_status

    @property
    def last_time(self):
        """ 最后一次检测时间 """
        return self._last_time

    @property
    def https(self):
        """ 是否支持https """
        return self._https

    @property
    def type(self) -> str:
        """ 获取代理的协议类型 """
        return self._type.lower()

    @property
    def to_dict(self):
        """ 属性字典 """
        return {"proxy": self.proxy,
                "https": self.https,
                "fail_count": self.fail_count,
                "region": self.region,
                "anonymous": self.anonymous,
                "source": self.source,
                "check_count": self.check_count,
                "last_status": self.last_status,
                "last_time": self.last_time,
                "type": self.type
                }

    @property
    def to_json(self):
        """ 转化为json格式 """
        return json.dumps(self.to_dict, ensure_ascii=False)

    @fail_count.setter
    def fail_count(self, value):
        """测试此代理的失败次数"""
        self._fail_count = value

    @check_count.setter
    def check_count(self, value):
        """测试此代理的次数"""
        self._check_count = value

    @last_status.setter
    def last_status(self, value):
        self._last_status = value

    @last_time.setter
    def last_time(self, value):
        """上次检测时间"""
        self._last_time = value

    @https.setter
    def https(self, value):
        """返回 True 如果是https 类型的代理，否则返回 False """
        self._https = value

    def add_source(self, source_str):
        """ 返回代理的来源，使用‘/’ 分隔，多个代理网站可能会包含同一个代理ip  """
        if source_str:
            self._source += "/" + source_str
