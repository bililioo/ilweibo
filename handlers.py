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

@post('/api/weibo')
async def api_weibo(*, pageIndex):
    if not pageIndex or not pageIndex.strip():
        raise APIValueError('pageIndex')

    pageIndex = int(pageIndex) * 20
    weibo_arr = await models.weibo.findAll(limit=(pageIndex, 20))
    return {'data': weibo_arr, 'count': len(weibo_arr)}

@post('/api/comments')
async def api_comments(*, pageIndex):
    if not pageIndex or not pageIndex.strip():
        raise APIValueError('pageIndex')

    pageIndex = int(pageIndex) * 20
    comment_arr = await models.comment.findAll(limit=(pageIndex, 20))
    return {'data': comment_arr, 'count': len(comment_arr)}
    

@post('/api/report')
def aip_report(*, isWeibo, id, r_uid):
    
    url = 'http://service.account.weibo.com/aj/reportspamobile'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://service.account.weibo.com',
        'Host': 'service.account.weibo.com',
        'Accept': '*/*', 
        'Connection': 'keep-alive', 
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': 'SER=usrmdinst_7; ALF=1528523211; SUB=_2A25396ybDeRhGeRN71cU9CjEwjuIHXVVGzTTrDV8PUJbkNBeLWPykW1NU47RsmJVZMKE0v4PAxEfDF2Ls82BAcrL; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWr61b0KdPzp7BYCG.-4ST_5JpX5oz75NHD95QEe0BfSKBc1h.NWs4DqcjiBJLjIgpDdcva; ULV=1525919228138:18:2:2:6036951897751.944.1525919228069:1525916780738; SUHB=0z1xxCzf3K2UGo; wvr=6; UOR=,,www.arefly.com; SCF=As0BWSjh1dAM17WuhXQaESX4L8LgKvwxiXvNhF2dEwfOcPSIavRa7P7yrrX2T_BGc_SDA-z1wQeIb0q3rTEV-6U.; SINAGLOBAL=5033181860449.794.1490265215741',
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
        return response.text
    except Exception as error:
        logging.info(error)
        return {"code" : "500","msg" : "程序错误"} 
    