 #!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ben'

import logging; logging.basicConfig(level=logging.INFO)

import requests
import datetime
import time
import json
import urllib

def get_search(word):
#     curl 'http://s.weibo.com/ajax/pic/list?search=%2525E5%25258D%252596%2525E7%252589%252587&page=3&_t=0&__rnd=1528685316536' \
# -XGET \
# -H 'Content-Type: application/x-www-form-urlencoded' \
# -H 'Host: s.weibo.com' \
# -H 'Accept: */*' \
# -H 'Connection: keep-alive' \
# -H 'Accept-Language: zh-cn' \
# -H 'Accept-Encoding: gzip, deflate' \
# -H 'Cookie: WBStorage=5548c0baa42e6f3d|undefined; SWB=usrmdinst_18; wvr=6; ALF=1560221107; SSOLoginState=1528685108; SUB=_2A252GZJjDeRhGeRN71cU9CjEwjuIHXVVboSrrDV8PUNbmtBeLRT1kW9NU47RsoW1NeG1nhNyfCFgAAi6GyRmxwcr; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWr61b0KdPzp7BYCG.-4ST_5JpX5KzhUgL.Foz0Sh-fShqR1KM2dJLoI7LFIgpDdsLadcYt; SUHB=0la0Isa2cAj6Ix; Apache=4189798176388.675.1528685080650; SINAGLOBAL=4189798176388.675.1528685080650; ULV=1528685080654:1:1:1:4189798176388.675.1528685080650:; SWBSSL=usrmdinst_19; _s_tentry=passport.weibo.com; cross_origin_proto=SSL; login_sid_t=fd8b740a21b4dc6e2de19a638a877d33' \
# -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15' \
# 'Referer: http://s.weibo.com/pic/%25E5%258D%2596%25E7%2589%2587&Refer=weibo_pic' \
# 'X-Requested-With: XMLHttpRequest'
    a = datetime.datetime.now().timestamp()
    a = int(a * 1000)
    logging.info(a)

    # 奇葩渣浪，三次url编码
    word = urllib.parse.quote(word)
    word = urllib.parse.quote(word)
    word = urllib.parse.quote(word)

    url = 'http://s.weibo.com/ajax/pic/list?search=%s&page=3&_t=0&__rnd=%s' % (word, a)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 's.weibo.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': 'WBStorage=5548c0baa42e6f3d|undefined; SWB=usrmdinst_18; wvr=6; ALF=1560221107; SSOLoginState=1528685108; SUB=_2A252GZJjDeRhGeRN71cU9CjEwjuIHXVVboSrrDV8PUNbmtBeLRT1kW9NU47RsoW1NeG1nhNyfCFgAAi6GyRmxwcr; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWr61b0KdPzp7BYCG.-4ST_5JpX5KzhUgL.Foz0Sh-fShqR1KM2dJLoI7LFIgpDdsLadcYt; SUHB=0la0Isa2cAj6Ix; Apache=4189798176388.675.1528685080650; SINAGLOBAL=4189798176388.675.1528685080650; ULV=1528685080654:1:1:1:4189798176388.675.1528685080650:; SWBSSL=usrmdinst_19; _s_tentry=passport.weibo.com; cross_origin_proto=SSL; login_sid_t=fd8b740a21b4dc6e2de19a638a877d33',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
        'Referer': 'http://s.weibo.com/pic/%s&Refer=weibo_pic' % word,
        'X-Requested-With': 'XMLHttpRequest',
    }

    response = requests.get(url, headers=headers)
    
    json_dict = response.json()




if __name__ == '__main__':  
    get_search('卖片')
