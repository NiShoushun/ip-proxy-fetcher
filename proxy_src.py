# -*- coding: utf-8 -*-

import re
from time import sleep

from util.webRequest import WebRequest

"""
函数返回(proxy, proxy_type, anonymous, region)
"""


def freeProxy01():
    """
    米扑代理 https://proxy.mimvp.com/ 只能访问第一页免费ip
    :return:
    """
    url_list = [
        'https://proxy.mimvp.com/freeopen?proxy=in_hp',
        'https://proxy.mimvp.com/freeopen?proxy=out_hp',
        'https://proxy.mimvp.com/freeopen?proxy=in_socks'
    ]
    port_img_map = {'DMxMjg': '3128', 'Dgw': '80', 'DgwODA': '8080',
                    'DgwOA': '808', 'DgwMDA': '8000', 'Dg4ODg': '8888',
                    'DgwODE': '8081', 'Dk5OTk': '9999'}
    for url in url_list:
        html_tree = WebRequest().get(url).tree
        for tr in html_tree.xpath(".//table[@class='mimvp-tbl free-proxylist-tbl']/tbody/tr"):
            try:
                ip = ''.join(tr.xpath('./td[2]/text()'))
                port_img = ''.join(tr.xpath('./td[3]/img/@src')).split("port=")[-1]
                port = port_img_map.get(port_img[14:].replace('O0O', ''))
                proxy_type = ''.join(tr.xpath('./td[4]/text()'))
                anonymous = ''.join(tr.xpath('./td[5]/text()'))
                if port:
                    yield ip + ":" + port, proxy_type, anonymous, ""
            except Exception as e:
                break


def freeProxy02():
    """
    代理66 http://www.66ip.cn/
    :return:
    """
    url = "http://www.66ip.cn/mo.php"

    resp = WebRequest().get(url, timeout=10)
    proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})', resp.text)
    for proxy in proxies:
        anonymous = ""
        proxy_type = ""
        region = ""
        yield proxy, proxy_type, anonymous, region


def freeProxy03():
    """ 开心代理 """
    target_urls = ["http://www.kxdaili.com/dailiip/1/", "http://www.kxdaili.com/dailiip/2/"]
    max_page = 10

    for url in target_urls:
        for i in range(1, max_page + 1):
            tree = WebRequest().get(url + f"{i}.html").tree
            for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                ip = "".join(tr.xpath('./td[1]/text()')).strip()
                port = "".join(tr.xpath('./td[2]/text()')).strip()
                proxy = "%s:%s" % (ip, port)
                anonymous = "".join(tr.xpath('./td[3]/text()')).strip()
                proxy_type = "".join(tr.xpath('./td[4]/text()')).strip()
                region = "".join(tr.xpath('./td[6]/text()')).strip()

                yield proxy, proxy_type, anonymous, region


def freeProxy04():
    """ 蝶鸟IP https://www.dieniao.com/FreeProxy/2.html"""
    url = "https://www.dieniao.com/FreeProxy.html"
    max_page = 10
    for i in range(10):
        tree = WebRequest().get(url, verify=False).tree
        for li in tree.xpath("//div[@class='free-main col-lg-12 col-md-12 col-sm-12 col-xs-12']/ul/li")[1:]:
            ip = "".join(li.xpath('./span[1]/text()')).strip()
            port = "".join(li.xpath('./span[2]/text()')).strip()
            proxy = "%s:%s" % (ip, port)
            proxy_type = ""
            anonymous = "".join(li.xpath('./span[3]/text()')).strip()
            region = "".join(li.xpath('./span[4]/text()')).strip()
            server = "".join(li.xpath('./span[5]/text()')).strip()
            yield proxy, proxy_type, anonymous, region + " " + server


def freeProxy05():
    """ 快代理 https://www.kuaidaili.com """
    url_pattern = [
        'https://www.kuaidaili.com/free/inha/',
        'https://www.kuaidaili.com/free/intr/'
    ]
    max_page = 4329
    for url in url_pattern:
        for i in range(1, max_page + 1):
            try:
                tree = WebRequest().get(url + f"{i}").tree
                proxy_list = tree.xpath('.//table//tr')
                sleep(1)  # 必须sleep 不然第二条请求不到数据
                for tree in proxy_list[1:]:
                    proxy = ':'.join(tree.xpath('./td/text()')[0:2])
                    anonymous = "".join(tree.xpath('./td[2]/text()')).strip()
                    proxy_type = "".join(tree.xpath('./td[3]/text()')).strip()
                    region = "".join(tree.xpath('./td[4]/text()')).strip()
                    yield proxy, proxy_type, anonymous, region
            except Exception:
                break


def freeProxy06():
    """ PROXY11 https://proxy11.com """
    url = "https://proxy11.com/api/demoweb/proxy.json?country=hk&speed=2000"
    try:
        resp_json = WebRequest().get(url).json
        for each in resp_json.get("data", []):
            proxy = "%s:%s" % (each.get("ip", ""), each.get("port", ""))
            proxy_type = ""
            anonymous = ""
            region = each.get("country", "")
            yield proxy, proxy_type, anonymous, region
    except Exception as e:
        return


def freeProxy07():
    """ 云代理 """
    urls = ['http://www.ip3366.net/free/?stype=1', "http://www.ip3366.net/free/?stype=2"]
    max_page = 7
    for url in urls:
        try:
            for i in range(1, max_page + 1):
                r = WebRequest().get(url + f"&page={i}", timeout=10)
                # proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
                # for proxy in proxies:
                #
                #     yield ":".join(proxy)
                tree = r.tree
                proxy_list = tree.xpath('.//table//tr')
                sleep(1)  # 必须sleep 不然第二条请求不到数据
                for tree in proxy_list[1:]:
                    ip = "".join(tree.xpath('./td[1]/text()'))
                    port = "".join(tree.xpath('./td[2]/text()'))
                    proxy = ip + ":" + port
                    anonymous = "".join(tree.xpath('./td[3]/text()')).strip()
                    proxy_type = "".join(tree.xpath('./td[4]/text()')).strip()
                    region = "".join(tree.xpath('./td[5]/text()')).strip()
                    yield proxy, proxy_type, anonymous, region
        except Exception as e:
            break


def freeProxy08():
    """ 小幻代理 """
    urls = ['https://ip.ihuan.me/address/5Lit5Zu9.html']
    for url in urls:
        r = WebRequest().get(url, timeout=10)
        # proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
        # for proxy in proxies:
        #
        #     yield ":".join(proxy)
        tree = r.tree
        proxy_list = tree.xpath('.//table//tr')
        print(proxy_list)
        for tree in proxy_list[1:]:
            ip = "".join(tree.xpath('./td[1]/text()'))
            port = "".join(tree.xpath('./td[2]/text()'))
            proxy = ip + ":" + port
            anonymous = "".join(tree.xpath('./td[3]/text()')).strip()
            proxy_type = "".join(tree.xpath('./td[4]/text()')).strip()
            region = "".join(tree.xpath('./td[5]/text()')).strip()
            print(ip,port,proxy,anonymous,proxy_type,region)
            yield proxy, proxy_type, anonymous, region


def freeProxy09():
    """ 89免费代理 """
    max_page = 50
    for i in range(1, max_page + 1):
        r = WebRequest().get("https://www.89ip.cn/index_{i}.html", timeout=10)
        # proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
        # for proxy in proxies:
        #
        #     yield ":".join(proxy)
        tree = r.tree
        proxy_list = tree.xpath('.//table//tr')
        sleep(1)  # 必须sleep 不然第二条请求不到数据
        for tree in proxy_list[1:]:
            ip = "".join(tree.xpath('./td[1]/text()')).strip()
            port = "".join(tree.xpath('./td[2]/text()')).strip()
            proxy = ip + ":" + port
            anonymous = ""
            proxy_type = ""
            region = "".join(tree.xpath('./td[3]/text()')).strip()
            server = "".join(tree.xpath('./td[4]/text()')).strip()

            yield proxy, proxy_type, anonymous, region+" "+server

    # @staticmethod
    # def wallProxy01():
    #     """
    #     PzzQz https://pzzqz.com/
    #     """
    #     from requests import Session
    #     from lxml import etree
    #     session = Session()
    #     try:
    #         index_resp = session.get("https://pzzqz.com/", timeout=20, verify=False).text
    #         x_csrf_token = re.findall('X-CSRFToken": "(.*?)"', index_resp)
    #         if x_csrf_token:
    #             data = {"http": "on", "ping": "3000", "country": "cn", "ports": ""}
    #             proxy_resp = session.post("https://pzzqz.com/", verify=False,
    #                                       headers={"X-CSRFToken": x_csrf_token[0]}, json=data).json()
    #             tree = etree.HTML(proxy_resp["proxy_html"])
    #             for tr in tree.xpath("//tr"):
    #                 ip = "".join(tr.xpath("./td[1]/text()"))
    #                 port = "".join(tr.xpath("./td[2]/text()"))
    #                 yield "%s:%s" % (ip, port)
    #     except Exception as e:
    #         print(e)

    # @staticmethod
    # def freeProxy10():
    #     """
    #     墙外网站 cn-proxy
    #     :return:
    #     """
    #     urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)

    # @staticmethod
    # def freeProxy11():
    #     """
    #     https://proxy-list.org/english/index.php
    #     :return:
    #     """
    #     urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
    #     request = WebRequest()
    #     import base64
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
    #         for proxy in proxies:
    #             yield base64.b64decode(proxy).decode()

    # @staticmethod
    # def freeProxy12():
    #     urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)
