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

    statuses1 = ''' curl -H 'Host: api.weibo.cn' -H 'X-Sessionid: 5CBC6F87-A278-48AC-9655-51B0EDF638A1' -H 'Content-Type: application/x-www-form-urlencoded; charset=utf-8' -H 'cronet_rid: 6281642' -H 'SNRT: normal' -H 'X-Log-Uid: 5905727185' -H 'X-Validator: 6Vzq2VgU8V6Ar1xRCulvMt9Q1V7Ffz//aRoNKezzico=' -H 'User-Agent: Weibo/27683 (iPhone; iOS 11.3.1; Scale/3.00)' -H 'Accept: */*' --data-binary "refresh=pulldown&group_id=1028032288&extparam=discover%7Cnew_feed&fid=102803_ctg1_2288_-_ctg1_2288&lon=113.262150&uicode=10000495&count=25&trim_level=1&trim_page_recom=0&containerid=102803_ctg1_2288_-_ctg1_2288&fromlog=1028032288&uid=5905727185&luicode=10000001&featurecode=10000001&refresh_sourceid=10000001&preAdInterval=-1&lat=23.152033&since_id=0&need_jump_scheme=1" --compressed 'https://api.weibo.cn/2/statuses/unread_hot_timeline?gsid=_2A252BIQPDeRxGeNH61cW8inNwzmIHXVSk5DHrDV6PUJbkdANLUSikWpNSvHTrCNBd2IXIL_F3bcLbMsB374S9qk5&wm=3333_2001&i=ad94a29&b=0&from=1085193010&c=iphone&networktype=wifi&v_p=60&skin=default&v_f=1&s=8e5ddddd&lang=zh_CN&sflag=1&ua=iPhone10,3__weibo__8.5.1__iphone__os11.3.1&ft=0&aid=01Am3uxcoYaVGEmHeFJ4aOVd-t8PceFQf7qDeNrrSTV1URSjw.' 2>/dev/null '''

    friendship1 = ''' curl -H 'Host: api.weibo.cn' -H 'User-Agent: Weibo/27683 (iPhone; iOS 11.3.1; Scale/3.00)' -H 'X-Validator: 6Vzq2VgU8V6Ar1xRCulvMt9Q1V7Ffz//aRoNKezzico=' -H 'X-Sessionid: 1D12AE8B-7BA3-4F2F-B655-A48A31CE2A47' -H 'X-Log-Uid: 5905727185' -H 'cronet_rid: 2434869' -H 'SNRT: normal' -H 'Accept: */*' --compressed 'https://api.weibo.cn/2/Page/Friendship/Accounttimeline?gsid=_2A252BIQPDeRxGeNH61cW8inNwzmIHXVSk5DHrDV6PUJbkdANLUSikWpNSvHTrCNBd2IXIL_F3bcLbMsB374S9qk5&wm=3333_2001&i=ad94a29&b=0&from=1085193010&c=iphone&networktype=wifi&v_p=60&skin=default&v_f=1&s=8e5ddddd&lang=zh_CN&sflag=1&ua=iPhone10,3__weibo__8.5.1__iphone__os11.3.1&ft=0&aid=01Am3uxcoYaVGEmHeFJ4aOVd-t8PceFQf7qDeNrrSTV1URSjw.&idnum=0&card_type=1101&mobile=0' 2>/dev/null '''

    statuses2 = ''' curl -H 'Host: api.weibo.cn' -H 'X-Sessionid: EFCD0AEF-421A-44F5-BD07-F1CE523ED2C7' -H 'Content-Type: application/x-www-form-urlencoded; charset=utf-8' -H 'cronet_rid: 10632795' -H 'SNRT: normal' -H 'X-Log-Uid: 5905727185' -H 'X-Validator: 7pniXbmDXCuhgCKPdspgbkCxVnm2vK4tqdoO9KDJ9Vk=' -H 'User-Agent: Weibo/27683 (iPhone; iOS 11.3.1; Scale/3.00)' -H 'Accept: */*' --data-binary "group_id=1028032288&extparam=discover%7Cnew_feed&fid=102803_ctg1_2288_-_ctg1_2288&lon=113.262150&uicode=10000495&count=25&trim_level=1&max_id=1&trim_page_recom=0&containerid=102803_ctg1_2288_-_ctg1_2288&fromlog=1028032288&uid=5905727185&luicode=10000001&featurecode=10000001&refresh_sourceid=10000001&lat=23.152033&lastAdInterval=-1&need_jump_scheme=1" --compressed 'https://api.weibo.cn/2/statuses/unread_hot_timeline?gsid=_2A252BIQPDeRxGeNH61cW8inNwzmIHXVSk5DHrDV6PUJbkdANLUSikWpNSvHTrCNBd2IXIL_F3bcLbMsB374S9qk5&wm=3333_2001&i=ad94a29&b=0&from=1085193010&c=iphone&networktype=wifi&v_p=60&skin=default&v_f=1&s=8e5ddddd&lang=zh_CN&sflag=1&ua=iPhone10,3__weibo__8.5.1__iphone__os11.3.1&ft=0&aid=01Am3uxcoYaVGEmHeFJ4aOVd-t8PceFQf7qDeNrrSTV1URSjw.' 2>/dev/null '''

    unread_count = ''' curl -H 'Host: api.weibo.cn' -H 'User-Agent: Weibo/27683 (iPhone; iOS 11.3.1; Scale/3.00)' -H 'X-Validator: /mu4ZGMlP4BbplT+3lY3UPH/iSfazJFBqP07o5IQaxI=' -H 'X-Sessionid: 31E30EF7-AE71-4BD1-BF1B-E95F59D2AFE0' -H 'X-Log-Uid: 5905727185' -H 'cronet_rid: 2736932' -H 'SNRT: normal' -H 'Accept: */*' --compressed 'https://api.weibo.cn/2/remind/unread_count?wm=3333_2001&i=ad94a29&b=0&from=1085193010&c=iphone&networktype=wifi&v_p=60&skin=default&v_f=1&lang=zh_CN&sflag=1&ua=iPhone10,3__weibo__8.5.1__iphone__os11.3.1&ft=0&aid=01Am3uxcoYaVGEmHeFJ4aOVd-t8PceFQf7qDeNrrSTV1URSjw.&with_page_group=1&with_settings=1&s=8e5ddddd&with_comment_attitude=1&gsid=_2A252BIQPDeRxGeNH61cW8inNwzmIHXVSk5DHrDV6PUJbkdANLUSikWpNSvHTrCNBd2IXIL_F3bcLbMsB374S9qk5&with_common_cmt=1' 2>/dev/null '''

    arr = [
        {'statuses': statuses1, 'other': friendship1},
        {'statuses': statuses2, 'other': unread_count}
    ]

    try:
        response = json.loads(subprocess.getoutput(statuses1))
        fs = json.loads(subprocess.getoutput(friendship1))
        await get_weibo(response)

        await asyncio.sleep(300)

        response2 = json.loads(subprocess.getoutput(statuses2))
        unread = json.loads(subprocess.getoutput(unread_count))
        await get_weibo(response2)

    except Exception as error:
        logging.info('<<<<<<<<<<<<<<< error:%s' % error)

async def get_weibo(response):

    # cmd = ''' curl -H 'Host: api.weibo.cn' -H 'X-Sessionid: 047BEA3F-E290-4316-9628-35848E4BC5F2' -H 'Content-Type: application/x-www-form-urlencoded; charset=utf-8' -H 'cronet_rid: 6428596' -H 'SNRT: normal' -H 'X-Log-Uid: 2345546897' -H 'X-Validator: oVyKhct/EWPSNnnjorVNq4dy1K4uKsxjBVlKA4dtUn8=' -H 'User-Agent: Weibo/27222 (iPhone; iOS 11.3.1; Scale/3.00)' -H 'Accept: */*' --data-binary "group_id=1028032288&extparam=discover%7Cnew_feed&fid=102803_ctg1_2288_-_ctg1_2288&lon=113.318250&uicode=10000495&count=25&trim_level=1&max_id=2&trim_page_recom=0&containerid=102803_ctg1_2288_-_ctg1_2288&fromlog=1028032288&uid=2345546897&luicode=10000001&featurecode=10000001&refresh_sourceid=10000001&lat=23.124061&lastAdInterval=-1&need_jump_scheme=1" --compressed 'https://api.weibo.cn/2/statuses/unread_hot_timeline?gsid=_2A253-VPwDeRxGeRN71cU9CjEwjuIHXVSr-A4rDV6PUJbkdAKLRDVkWpNU47Rsns5Cfo-vL5qPzjVqe10vlymoLlb&wm=3333_2001&i=ad94a29&b=0&from=1084393010&c=iphone&networktype=wifi&v_p=60&skin=default&v_f=1&s=aaaaaaaa&lang=zh_CN&sflag=1&ua=iPhone10,3__weibo__8.4.3__iphone__os11.3.1&ft=0&aid=01Am3uxcoYaVGEmHeFJ4aOVd8YJYEVuvFQiNIrDPm2ss_m5vg.'  2>/dev/null '''  

    # try:
    #     result = json.loads(subprocess.getoutput(cmd))
    # except Exception as error:
    #     logging.info('<<<<<<<<<<<<<<< error:%s' % error)
    #     return 

    statuses = response.get('statuses', None)

    if statuses == None:
        return
    
    for item in statuses:
        id = item.get('id')
        comments_count = item.get('comments_count', '0')

        if int(comments_count) > 10:
            await get_comments(id, comments_count) 
            await asyncio.sleep(60)
            

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

        await asyncio.sleep(10)
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