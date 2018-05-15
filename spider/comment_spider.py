 #!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ben'

import logging; logging.basicConfig(level=logging.INFO)

from urllib import parse
from urllib import request
import requests
import asyncio
import urllib
from bs4 import BeautifulSoup
import time
import ssl
import models
from functools import reduce

ssl._create_default_https_context = ssl._create_unverified_context

async def hot_wb():
    '''
    热门微博
    '''

    url = 'https://m.weibo.cn/api/container/getIndex?containerid=102803'

    headers = {
        'Host': 'm.weibo.cn',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'br, gzip, deflate',
        'Cookie': 'MLOGIN=1; M_WEIBOCN_PARAMS=featurecode%3D20000320%26oid%3D4237460512348275%26luicode%3D20000061%26lfid%3D4237460512348275%26fid%3D102803%26uicode%3D10000011; WEIBOCN_FROM=1110006030; H5_INDEX=2; H5_INDEX_TITLE=Bililiooo; SCF=AjOJzMUpKNRc4sqxMp__70x4DbSoPaPY9rwsACWlPzjkN4ptz3fa8ri-Qsj0eeM1HCtWlvpVIl0_MpYHtdRRYJs.; SSOLoginState=1525919576; SUB=_2A253998IDeRhGeRN71cU9CjEwjuIHXVVG-FArDV6PUJbkdANLVPCkW1NU47RsgKuIDNjCgWCcPUbaErA3u_f0QTB; SUHB=0z1xxCzf3K2UGo; TMPTOKEN=NK0BAKjmvUlbXc7n0KVNUitHBLpqPQMxkhw9DGNHp2ShaBxPpzO6MTBFre18TSNV; _T_WM=bd324ce74a01f146dfcc272ebbbc5f45',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15' ,
        'Referer': 'https://m.weibo.cn/p/index?containerid=102803',
        'X-Requested-With': 'XMLHttpRequest'
    }

    response = requests.get(url, headers=headers)
    tmpJson = response.json()
    data = tmpJson['data']
    cards = data['cards']

    for item in cards:
        # 评论数超过2才加入队列中
        comments_count = item.get('mblog').get('comments_count')
        if comments_count >= 2:
            try:
                id = item.get('mblog').get('id')
                await get_comments(id, comments_count)
            except Exception as error:
                logging.info('<<<<<<<<<<<<<<< error:%s' % error)

            

async def get_comments(id, comments):
    '''
    评论
    '''
    time.sleep(1)

    page_count = int(comments / 10) + 1
    
    cookie = 'MLOGIN=1; M_WEIBOCN_PARAMS=featurecode%%3D20000320%%26oid%%3D%s%%26luicode%%3D10000011%%26lfid%%3D1076031791709041%%26uicode%%3D20000061%%26fid%%3D%s; WEIBOCN_FROM=1110006030; SSOLoginState=1525931210; SUB=_2A25396yaDeRhGeRN71cU9CjEwjuIHXVVGzTSrDV6PUJbkdANLWfukW1NU47RslnWkS5f5K-NHkB62C58p0Bnegav; SUHB=0WGtKITH-S-Yul; H5_INDEX=2; H5_INDEX_TITLE=Bililiooo; SCF=AjOJzMUpKNRc4sqxMp__70x4DbSoPaPY9rwsACWlPzjkN4ptz3fa8ri-Qsj0eeM1HCtWlvpVIl0_MpYHtdRRYJs.; _T_WM=bd324ce74a01f146dfcc272ebbbc5f45' % (id, id)

    referer = 'https://m.weibo.cn/status/%s' % id
    logging.info('当前微博：%s', referer)
    headers = {
        'Host': 'm.weibo.cn',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'br, gzip, deflate',
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
        'Referer': referer,
        'X-Requested-With': 'XMLHttpRequest',
    }

    items = []
    for page in range(1, page_count):
        url = 'https://m.weibo.cn/api/comments/show?id=%s&page=%s' % (id, page)
        logging.info('当前评论页：%s' % url)
        response = requests.get(url, headers=headers)   
        data = response.json().get('data')
        
        if data.get('data') != None:
            for item in data.get('data'):
                if item.get('pic'):
                    items.append(item)

        if data.get('hot_data') != None:
            for hot_item in data.get('hot_data'):
                if hot_item.get('pic'):
                    items.append(hot_item)
    
    for item in items:
        id = item.get('id')
        r_uid = item.get('user').get('id')
        name = item.get('user').get('screen_name')
        pic = item['pic']['url']
        text = item.get('text')

        model = models.comment(id=id, name=name, pic=pic, text=text, r_uid=r_uid)
        logging.info(model)
        await model.save()    

        