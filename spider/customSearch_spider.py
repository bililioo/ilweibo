#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ben'

import logging; logging.basicConfig(level=logging.INFO)

from urllib import parse
from urllib import request
import requests
import asyncio
import urllib
import time
import ssl
from functools import reduce
import models
import datetime
import re


async def search_weibo(keyword):
    try:
        await search(keyword)
    except Exception as error:
        logging.info('<<<<<<<<<<<<<<< error:%s' % error)
    

async def search(keyword):

    ref = {
        '100103type': '2',
        'q': keyword,
        'type': 'wb',
        'queryVal': keyword,
        'luicode': '10000011',
        'lfid': '106003type=1',
        'title': keyword
    }

    referer = 'https://m.weibo.cn/p/%s' % parse.urlencode(ref)

    header = {
        'Host': 'm.weibo.cn',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'br, gzip, deflate',
        'Cookie': 'MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D106003type%253D1%26fid%3D100103type%253D2%2526q%253D%25E5%258D%2596%25E7%2589%2587%26uicode%3D10000011; WEIBOCN_FROM=1110006030; H5_INDEX=1; H5_INDEX_TITLE=Bililiooo; SSOLoginState=1525931210; SUB=_2A25396yaDeRhGeRN71cU9CjEwjuIHXVVGzTSrDV6PUJbkdANLWfukW1NU47RslnWkS5f5K-NHkB62C58p0Bnegav; SUHB=0WGtKITH-S-Yul; SCF=AjOJzMUpKNRc4sqxMp__70x4DbSoPaPY9rwsACWlPzjkN4ptz3fa8ri-Qsj0eeM1HCtWlvpVIl0_MpYHtdRRYJs.; _T_WM=bd324ce74a01f146dfcc272ebbbc5f45',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
        'Referer': referer,
        'X-Requested-With': 'XMLHttpRequest'
    }

    weibo_url = 'https://m.weibo.cn/api/container/getIndex'

    for i in range(1, 25):

        await asyncio.sleep(2)

        params = {
            'type': 'wb',
            'queryVal': keyword,
            'luicode': '10000011',
            'lfid': '106003type=1%3D1',
            'title': keyword,
            'containerid': '100103type=2%%3D2%%26q%%3D%s' % keyword,
            'page': i,
        }

        logging.info("=========当前url: %s" % weibo_url)
        logging.info("=========当前参数: %s" % params)
        
        response = requests.get(weibo_url, params=params, headers=header)
        
        data = response.json().get('data')
        cards = data.get('cards')

        if len(cards) < 1:
            continue 

        card = cards[0]
        card_group = card.get('card_group')

        for card in card_group:
            mblog = card.get('mblog')

            id = mblog.get('id')
            name = mblog.get('user').get('screen_name')
            r_uid = mblog.get('user').get('id')
            text = mblog.get('text', '')
            pics = mblog.get('pics', [])

            t = datetime.datetime.now()
            text = re.sub(r'</?\w+[^>]*>', '', text)

            pic_arr = []
            for pic in pics:
                pic_url = pic.get('url', None)
                if pic_url != None:
                    pic_arr.append(pic_url)

            if len(pic_arr) == 0:
                continue 

            pic_str = ','.join(pic_arr)

            model = models.customWeibo(id=id, name=name, pic=pic_str, text=text, r_uid=r_uid, time=t)
            logging.info(model)
        
            try:
                await model.save()
            except Exception as error:
                logging.info('<<<<<<<<<<<<<<< error:%s' % error)
    

