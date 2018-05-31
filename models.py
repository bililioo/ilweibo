#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ben'

import orm
from orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField

class comment(Model):
    __table__ = 'comments'

    pic = StringField(ddl='text(200)')
    text = StringField(ddl='text(300)')
    name = StringField(ddl='text(30)')
    r_uid = StringField(ddl='text(200)')
    id = StringField(primary_key=True, ddl='text(200)')
    time = StringField()
    report = IntegerField()


class weibo(Model):
    __table__ = 'weibo'

    pic = StringField(ddl='text(200)')
    text = StringField(ddl='text(300)')
    name = StringField(ddl='text(30)')
    r_uid = StringField(ddl='text(200)')
    id = StringField(ddl='text(200)')
    index = IntegerField(primary_key=True)
    time = StringField()
    report = IntegerField()

class customWeibo(Model):
    __table__ = 'customWeibo'

    pic = StringField(ddl='text()')
    text = StringField(ddl='text(300)')
    name = StringField(ddl='text(30)')
    r_uid = StringField(ddl='text(200)')
    id = StringField(ddl='text(200)')
    index = IntegerField(primary_key=True)
    time = StringField()
    report = IntegerField()