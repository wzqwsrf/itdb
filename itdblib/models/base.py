# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from qg.db import models
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base(cls=models.ModelBase)
