#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ben'

import logging; logging.basicConfig(level=logging.INFO)

import orm
import asyncio
import os, json
from config import configs
import parameters
import models
import ast
import random
from coroweb import add_routes, add_static
from aiohttp import web
from spider import search_spider
from spider import comment_spider
import time
import datetime

async def logger_factory(app, handler):
    async def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        return (await handler(request))
    return logger

async def response_factory(app, handler):
    async def response(request):
        r = await handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        if isinstance(r, int) and r >= 100 and r < 600:
            return web.Response(r)
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                return web.Response(t, str(m))
        # default:
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response

async def init_sql(loop):
    logging.info(configs)
    await orm.create_pool(loop, **configs.db)


async def init(loop):

    app = web.Application(loop=loop, middlewares=[logger_factory, response_factory])
    add_routes(app, 'handlers')

    srv = await loop.create_server(app.make_handler(), configs.apis.get('host', 'localhost'), configs.apis['port'])
    logging.info('server started at %s:%s...' % (configs.apis['host'], configs.apis['port']))
    return srv

async def init_spider():
    
    while True:
        t = datetime.datetime.now()
        if t.hour > 1 and t.hour < 7:
            asyncio.sleep(3600)
        else:
            await search_spider.search_weibo('卖片')
            asyncio.sleep(3600)
            logging.info('睡一小时')

async def delay():
    s = random.randint(1, 5)
    await asyncio.sleep(s)

async def init_spider_1():
    while True:
        t = datetime.datetime.now()
        if t.hour > 1 and t.hor < 7:
            asyncio.sleep(3600)
        else:
            await comment_spider.get_hot_weibo()
            asyncio.sleep(900)
            logging.info('睡半小时')

task = [init_spider(), init_spider_1()]

loop = asyncio.get_event_loop()
loop.run_until_complete(init_sql(loop))
loop.run_until_complete(asyncio.wait(task))
# loop.run_until_complete(init(loop))
loop.run_forever()
