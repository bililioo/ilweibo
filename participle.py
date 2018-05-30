#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, codecs  
import jieba  
from collections import Counter  
import datetime
import asyncio
import datetime
import functools


class A(object):
    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    def __init__(self, birth):
        self.birth = birth

class CallTimesLimit(object):
    def __init__(self, max):
        print('init CallTimesLimit')
        self.__max = max
        self.__count = 0

    def __call__(self, fun):
        print("call __call__")
        self.__fun = fun
        return self.__proxy

    def __proxy(self, *args, **kwargs):
        print("proxy")
        self.__count += 1
        if self.__count > self.__max:
            print('adsfasdfasdf')
            raise Exception("{f} is called over {limit} times".format(f=self.__fun.__name__,
                                                                      limit=self.__max))
        else:
            self.__fun(*args, **kwargs)


import types
from functools import wraps

class Profiled:
    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

@Profiled
def add(x, y):
    return x + y



# @CallTimesLimit(3)
# def foo(x):
#     for a in range(10):
#         # @CallTimesLimit(3)
#         print(x)

def get(path):
    '''
    Define decorator @get('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (path, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator


if __name__ == '__main__':
    add(3, 3)
    add(5, 3)
    add(5, 3)
    add(5, 3)
    add(5, 3)
    add(5, 3)
    add(5, 3)
    add(5, 3)
    add(5, 3)
    add(5, 3)
    print(add.ncalls)
#     foo(2)
#     foo(2)
#     foo(2)
#     foo(2)
#     foo(2)

def get_words(txt):  
    seg_list = jieba.cut(txt)  
    c = Counter()  
    for x in seg_list:  
        if len(x)>1 and x != '\r\n':  
            c[x] += 1  
    print('常用词频度统计结果')  
    for (k,v) in c.most_common(100):  
        print('%s  %d' % (k, v)) 

@get('sdaf')
async def a():
    while True:
        print("睡十秒")
        await asyncio.sleep(1)

async def b():
    while True:
        print("睡两秒")
        await asyncio.sleep(2)

task = [a(), b()]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(task))
loop.run_forever()

# if __name__ == '__main__':  
#     # with codecs.open('/Users/chenbin/schumacher/分词文章.txt', 'r', 'utf8') as f:  
#     #     txt = f.read()  
#     # get_words(txt)  

#     print(datetime.datetime.now())
#     t = datetime.datetime.now()
#     print(t)

#     if t.hour < 8:
    