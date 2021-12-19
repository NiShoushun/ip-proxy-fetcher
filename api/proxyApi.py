# -*- coding: utf-8 -*-

"""
web api接口定义
"""

from werkzeug.wrappers import Response
from flask import Flask, jsonify, request

from core.proxy import Proxy
from core.dbhandler import DBHandler
from config.configuration import default_config as config
from util import logging, color

app = Flask(__name__)

proxy_handler = DBHandler()


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
    {"url": "/get", "params": "type: ''https'|'http'", "desc": "get a proxy"},
    {"url": "/pop", "params": "", "desc": "get and delete a proxy"},
    {"url": "/delete", "params": "proxy: 'e.g. 127.0.0.1:8080'",
     "desc": "delete an unable proxy"},
    {"url": "/all", "params": "type: ''https'|'http'",
     "desc": "get all proxy from proxy pool"},
    {"url": "/count", "params": "", "desc": "return proxy count"}
]


@app.route('/')
def index():
    return {'url': api_list}


@app.route('/get/')
def get():
    ptype = request.args.get("type", "").lower()
    proxy = proxy_handler.get(ptype)
    return proxy.to_dict if proxy else {"code": 0, "src": "no proxy"}


@app.route('/pop/')
def pop():
    ptype = request.args.get("type", "").lower()
    proxy = proxy_handler.pop(ptype)
    return proxy.to_dict if proxy else {"code": 0, "src": "no proxy"}


@app.route('/all/')
def getAll():
    ptype = request.args.get("type", "").lower()
    proxies = proxy_handler.getAll(ptype)
    return jsonify([_.to_dict for _ in proxies])


@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    status = proxy_handler.delete(Proxy(proxy))
    return {"status": status}


@app.route('/count/')
def getCount():
    status = proxy_handler.getCount()
    return status


def start():
    app.run(host=config.serverHost, port=config.serverPort)
