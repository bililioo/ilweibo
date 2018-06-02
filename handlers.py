#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' url handlers '

import logging; logging.basicConfig(level=logging.INFO)

from models import comment
from apis import APIValueError, APIResourceNotFoundError
from coroweb import get, post
from config import configs
from aiohttp import web
import aiohttp
import os
from datetime import datetime
import models
import requests

@post('/api/customweibo')
async def api_custom_weibo(*, pageIndex):
    if not pageIndex or not pageIndex.strip():
        raise APIValueError('pageIndex')

    pageIndex = int(pageIndex) * 20
    weibo_arr = await models.customWeibo.findAll(limit=(pageIndex, 20), orderBy='time desc')
    for item in weibo_arr:
        item.time = str(item.time)
    return {'data': weibo_arr, 'count': len(weibo_arr)}

@post('/api/weibo')
async def api_weibo(*, pageIndex):
    if not pageIndex or not pageIndex.strip():
        raise APIValueError('pageIndex')

    pageIndex = int(pageIndex) * 20
    weibo_arr = await models.weibo.findAll(limit=(pageIndex, 20), orderBy='time desc', where='report = 0')
    for weibo in weibo_arr:
        weibo.time = str(weibo.time)
    return {'data': weibo_arr, 'count': len(weibo_arr)}

@post('/api/comments')
async def api_comments(*, pageIndex):
    if not pageIndex or not pageIndex.strip():
        raise APIValueError('pageIndex')

    pageIndex = int(pageIndex) * 20
    comment_arr = await models.comment.findAll(limit=(pageIndex, 20), orderBy='time desc')
    for comment in comment_arr:
        comment.time = str(comment.time)

    return {'data': comment_arr, 'count': len(comment_arr)}
    

@post('/api/report')
async def aip_report(*, isWeibo, **kw):

    orderBy = kw.get('orderBy', None)
    id = kw.get('id', None)
    r_uid = kw.get('r_uid', None)
    pic = kw.get('pic', None)
    text = kw.get('text', None)
    name = kw.get('name', None)
    time = kw.get('time', None)
    index = kw.get('index', None)
    database_name = kw.get('db', None)

    url = 'http://service.account.weibo.com/aj/reportspamobile'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://service.account.weibo.com',
        'Host': 'service.account.weibo.com',
        'Accept': '*/*', 
        'Connection': 'keep-alive', 
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': 'SER=usrmdinst_6; SCF=An2bXdnAk8cjcDqTfmO7GGLsRKoz8iTLfjzcqWLoSn2Qp_ISyWZlwvbPULu6yBm-Kw..; SUB=_2A253-9ocDeRhGeRN71cU9CjEwjuIHXVVVoBUrDV8PUJbitANLVbgkWtNU47Rsky_qswzHE61wRLGITEA9t1-e6jd; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWr61b0KdPzp7BYCG.-4ST_5NHD95QEe0BfSKBc1h.NWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNeoeXSK-XSon4S7tt; SUHB=0YhgYlh4Es0Htq',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
        'Referer': 'http://service.account.weibo.com/reportspamobile?rid=4238111540751113&type=2&from=20000',
        'Content-Length': '128',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {
        'url': '',
        'type': '2',
        'rid': id,
        'uid': '2345546897',
        'r_uid': r_uid,
        'from': '20000',
        'getrid': id,
        'category': '2',
        'weiboGet': '0'
    }

    if isWeibo == '1':
        data = {
            'url': '',
            'type': '1',
            'rid': id,
            'uid': '2345546897',
            'r_uid': r_uid,
            'from': '20000',
            'getrid': id,
            'category': '2',
            'extra': '',
            'weiboGet': '0'
        }

    try:
        response = requests.post(url, headers=headers, data=data)
        logging.info(response.text)

        if isWeibo == '1':
            if database_name == 'weibo':
                w = await models.weibo.find(index)
                w.report = 1
                await w.update()
            else: 
                cw = await models.customWeibo.find(index)
                cw.report = 1
                await cw.update()
        else:
            c = await models.comment.find(id)
            c.report = 1
            await c.update()

        return response.text
    except Exception as error:
        logging.info(error)
        return {"code" : "500","msg" : "程序错误"} 
    