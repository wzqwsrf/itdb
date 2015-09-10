# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

def judge_key_not_null(params, key):
    if key in params and params[key] is not None and params[key] != '':
        return True
    return False