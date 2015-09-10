# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from datetime import datetime


# 获取当前时间
def get_now_date():
    return datetime.now()


def trans_time(curTime):
    format = '%Y-%m-%d %H:%M:%S'
    afterTime = "" if curTime is None else curTime.strftime(format)
    return afterTime
