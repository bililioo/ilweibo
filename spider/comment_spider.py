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

ssl._create_default_https_context = ssl._create_unverified_context

async def get_hot_weibo():

    cmd = ''' curl -H 'Host: api.weibo.cn' -H 'X-Sessionid: 047BEA3F-E290-4316-9628-35848E4BC5F2' -H 'Content-Type: application/x-www-form-urlencoded; charset=utf-8' -H 'cronet_rid: 6428596' -H 'SNRT: normal' -H 'X-Log-Uid: 2345546897' -H 'X-Validator: oVyKhct/EWPSNnnjorVNq4dy1K4uKsxjBVlKA4dtUn8=' -H 'User-Agent: Weibo/27222 (iPhone; iOS 11.3.1; Scale/3.00)' -H 'Accept: */*' --data-binary "group_id=1028032288&extparam=discover%7Cnew_feed&fid=102803_ctg1_2288_-_ctg1_2288&lon=113.318250&uicode=10000495&count=25&trim_level=1&max_id=2&trim_page_recom=0&containerid=102803_ctg1_2288_-_ctg1_2288&fromlog=1028032288&uid=2345546897&luicode=10000001&featurecode=10000001&refresh_sourceid=10000001&lat=23.124061&lastAdInterval=-1&need_jump_scheme=1" --compressed 'https://api.weibo.cn/2/statuses/unread_hot_timeline?gsid=_2A253-VPwDeRxGeRN71cU9CjEwjuIHXVSr-A4rDV6PUJbkdAKLRDVkWpNU47Rsns5Cfo-vL5qPzjVqe10vlymoLlb&wm=3333_2001&i=ad94a29&b=0&from=1084393010&c=iphone&networktype=wifi&v_p=60&skin=default&v_f=1&s=aaaaaaaa&lang=zh_CN&sflag=1&ua=iPhone10,3__weibo__8.4.3__iphone__os11.3.1&ft=0&aid=01Am3uxcoYaVGEmHeFJ4aOVd8YJYEVuvFQiNIrDPm2ss_m5vg.'  2>/dev/null '''  

    try:
        result = json.loads(subprocess.getoutput(cmd))
    except Exception as error:
        logging.info('<<<<<<<<<<<<<<< error:%s' % error)
        return 

    statuses = result.get('statuses', None)

    if statuses == None:
        return
    
    for item in statuses:
        id = item.get('id')
        comments_count = item.get('comments_count', '0')

        if int(comments_count) > 10:
            await get_comments(id, comments_count) 

            

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

        