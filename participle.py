#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, codecs  
import jieba  
from collections import Counter  
import datetime

def get_words(txt):  
    seg_list = jieba.cut(txt)  
    c = Counter()  
    for x in seg_list:  
        if len(x)>1 and x != '\r\n':  
            c[x] += 1  
    print('常用词频度统计结果')  
    for (k,v) in c.most_common(100):  
        print('%s  %d' % (k, v)) 


if __name__ == '__main__':  
    # with codecs.open('/Users/chenbin/schumacher/分词文章.txt', 'r', 'utf8') as f:  
    #     txt = f.read()  
    # get_words(txt)  

    print(datetime.datetime.now())
    t = datetime.datetime.now()
    print(t)

    if t.hour < 8:
    