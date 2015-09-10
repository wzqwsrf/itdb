# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


import sqlalchemy.types


class LTree(sqlalchemy.types.UserDefinedType):
    def get_col_spec(self):
        return 'LTREE'
