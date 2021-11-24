# -*- coding: utf-8 -*-

"""
web api接口定义
"""

import platform
from werkzeug.wrappers import Response
from flask import Flask, jsonify, request

from core.proxy import Proxy
from core.DB_handle import ProxyDBHandler
from config.configuration import default_config as config

app = Flask(__name__)

proxy_handler = ProxyDBHandler()


def iteritems(d, **kw):
    return iter(d.items(**kw))


class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (dict, list)):
            response = jsonify(response)

        return super(JsonResponse, cls).force_type(response, environ)


app.response_class = JsonResponse

api_list = [
    {"url": "/get", "params": "type: ''https'|''", "desc": "get a proxy"},
    {"url": "/pop", "params": "", "desc": "get and delete a proxy"},
    {"url": "/delete", "params": "proxy: 'e.g. 127.0.0.1:8080'",
     "desc": "delete an unable proxy"},
    {"url": "/all", "params": "type: ''https'|''",
     "desc": "get all proxy from proxy pool"},
    {"url": "/count", "params": "", "desc": "return proxy count"}
]


@app.route('/')
def index():
    return {'url': api_list}


@app.route('/get/')
def get():
    https = request.args.get("type", "").lower() == 'https'
    proxy = proxy_handler.get(https)
    return proxy.to_dict if proxy else {"code": 0, "src": "no proxy"}


@app.route('/pop/')
def pop():
    https = request.args.get("type", "").lower() == 'https'
    proxy = proxy_handler.pop(https)
    return proxy.to_dict if proxy else {"code": 0, "src": "no proxy"}


@app.route('/all/')
def getAll():
    https = request.args.get("type", "").lower() == 'https'
    proxies = proxy_handler.getAll(https)
    return jsonify([_.to_dict for _ in proxies])


@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    status = proxy_handler.delete(Proxy(proxy))
    return {"code": 0, "src": status}


@app.route('/count/')
def getCount():
    status = proxy_handler.getCount()
    return status


def start_server():
    app.run(host=config.serverHost, port=config.serverPort)
