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
    weibo_arr = await models.customWeibo.findAll(limit=(pageIndex, 20), orderBy='time desc', where='report = 0')
    for item in weibo_arr:
        item.time = str(item.time)
    return {'data': weibo_arr, 'count': len(weibo_arr)}

@post('/api/pcSearch')
async def api_pcSearch(*, pageIndex):
    if not pageIndex or not pageIndex.strip():
        raise APIValueError('pageIndex')

    pageIndex = int(pageIndex) * 20
    # weibo_arr = await models.weibo.findAll(limit=(pageIndex, 20), orderBy='time desc', where='report = 0')
    weibo_arr = await models.pc_search.findAll(limit=(pageIndex, 20), orderBy='time desc', where='report = 0')
    for weibo in weibo_arr:
        weibo.time = str(weibo.time)
    return {'data': weibo_arr, 'count': len(weibo_arr)}

@post('/api/weibo')
async def api_weibo(*, pageIndex):
    if not pageIndex or not pageIndex.strip():
        raise APIValueError('pageIndex')

    pageIndex = int(pageIndex) * 20
    weibo_arr = await models.weibo.findAll(limit=(pageIndex, 20), orderBy='time desc', where='report = 0')
    # weibo_arr = await models.pc_search.findAll(limit=(pageIndex, 20), orderBy='time desc', where='report = 0')
    for weibo in weibo_arr:
        weibo.time = str(weibo.time)
    return {'data': weibo_arr, 'count': len(weibo_arr)}

@post('/api/comments')
async def api_comments(*, pageIndex):
    if not pageIndex or not pageIndex.strip():
        raise APIValueError('pageIndex')

    pageIndex = int(pageIndex) * 20
    comment_arr = await models.comment.findAll(limit=(pageIndex, 20), orderBy='time desc', where='report = 0')
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
        'Cookie': 'SER=usrmdinst_10; Apache=422752374481.39215.1535721645090; ULV=1535721645100:6:4:2:422752374481.39215.1535721645090:1535269160919; _s_tentry=-; wvr=6; ALF=1536201481; SUB=_2A252bXZZDeRhGeRN71cU9CjEwjuIHXVVrhoRrDV8PUJbkNBeLXjzkW1NU47RspmcO_jyF4qc7JXHdpeLTppnYG6d; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWr61b0KdPzp7BYCG.-4ST_5JpX5oz75NHD95QEe0BfSKBc1h.NWs4DqcjiBJLjIgpDdcva; SCF=AjOJzMUpKNRc4sqxMp__70x4DbSoPaPY9rwsACWlPzjkvEkS3EhB7Foma3DglyzaOwFK7o4InHdSLeSNN0grEZA.; SUHB=0XDUe5Y3FggPHT; UOR=,,login.sina.com.cn; SINAGLOBAL=4189798176388.675.1528685080650',
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
        
        result = response.json()
        logging.info(result)
        if result['code'] == '100000' or '100003':
            if isWeibo == '1':
                if database_name == 'weibo':
                    w = await models.weibo.find(index)
                    w.report = 1
                    await w.update()
                elif database_name == 'pc_search':
                    w = await models.pc_search.find(index)
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
            
        # logging.info(response.text.encode('utf-8').decode('unicode_escape'))
        return response.text
    except Exception as error:
        logging.info(error)
        return {"code" : "500","msg" : "程序错误"} 
    

@post('/api/delete')
async def api_delete(*, index, db):
    if db == 'weibo':
        wb = await models.weibo.find(index)
        await models.weibo.remove(wb)

        return {'msg': '删除成功'}
    else:
        return {'msg': '删除失败'}