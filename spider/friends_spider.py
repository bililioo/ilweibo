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
import models
import json
import subprocess
import re
import datetime
import os

ssl._create_default_https_context = ssl._create_unverified_context

async def get_friends(next_cursor=None):

    frequency_path = os.getcwd() + '/spider/frequency.txt'

    with open(frequency_path, 'r') as f:
        # print(f.read())
        times = int(f.read())

    if times < 5:
        times += 1
        with open(frequency_path, 'w') as f:
            f.write('{0}'.format(times))
    else: 
        with open(frequency_path, 'w') as f:
            f.write('0')
        return

    headers = {
        'Host': 'm.weibo.cn',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'br, gzip, deflate',
        'Cookie': 'MLOGIN=1; M_WEIBOCN_PARAMS=featurecode%3D20000320%26oid%3D4243196316136299%26luicode%3D20000174%26lfid%3Dhotword%26uicode%3D20000174%26fid%3Dhotword; SCF=Apx5eBzew41Xy1bxo7TFV4M6UFtNK98yYu1tMgrz8LQu_HzWI_-5nkRPn_b97Iyy-z-i4TtN4gxMHb6fXcZfF-I.; SSOLoginState=1527147749; SUB=_2A252Ahy1DeRhGeNH61cW8inNwzmIHXVVDKT9rDV6PUJbkdANLRWkkW1NSvHTrFoVIxHBnoRgm8Y435KpOHAaiZ2Y; SUHB=0IIl5ghO8hTKQ9; H5_wentry=H5; WEIBOCN_WM=3349; backURL=http%3A%2F%2Fm.weibo.cn%2F; _T_WM=57a892b33b8998e33788fd682e2d3c1f',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
        'Referer': 'https://m.weibo.cn/',
        'X-Requested-With': 'XMLHttpRequest'
    }

    url = 'https://m.weibo.cn/feed/friends?version=v4'

    if next_cursor != None:
        url = 'https://m.weibo.cn/feed/friends?version=v4&next_cursor=%s&page=1' % next_cursor

    logging.info('当前feed流：%s' % url)
    try:
        response = requests.get(url, headers=headers)   
    except Exception as error:
        logging.info('<<<<<<<<<<<<<<< error:%s' % error)
        return 

    data = response.json()

    for item in data:
        card_group = item.get('card_group', [])
        cursor = item.get('next_cursor', None)

        for card in card_group:
            mblog = card.get('mblog', None)
            if mblog != None:
                id = mblog.get('id', None)
                comments_count = mblog.get('comments_count', '0')
                await asyncio.sleep(10)
                await get_comments(id, comments_count)

    await asyncio.sleep(10)
    await get_friends(next_cursor=cursor)


async def get_comments(id, comments):
    '''
    评论
    '''
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

        # 只采前3页
        if page > 3:
            return

        
        url = 'https://m.weibo.cn/api/comments/show?id=%s&page=%s' % (id, page)
        logging.info('当前评论页：%s' % url)
        response = requests.get(url, headers=headers)   
        data = response.json().get('data', None)

        if data == None:
            return 
        
        if data.get('data', None) != None:
            for item in data.get('data'):
                if item.get('pic'):
                    items.append(item)

        if data.get('hot_data', None) != None:
            for hot_item in data.get('hot_data'):
                if hot_item.get('pic'):
                    items.append(hot_item)

        await asyncio.sleep(4)
    
    if len(items) == 0:
        logging.info('------------没有图片评论')
    else:
        logging.info('------------图片评论有%d条' % len(items))

    for item in items:
        id = item.get('id')
        r_uid = item.get('user').get('id')
        name = item.get('user').get('screen_name')
        pic = item['pic']['url']
        text = item.get('text')

        try:
            text = re.sub(r'</?\w+[^>]*>', '', text)
            t = datetime.datetime.now()

            model = models.comment(id=id, name=name, pic=pic, text=text, r_uid=r_uid, time=t)
            logging.info(model)
            await model.save()    
        except Exception as error:
            logging.info('<<<<<<<<<<<<<<< error:%s' % error)
