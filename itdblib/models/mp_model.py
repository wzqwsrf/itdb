# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from sqlalchemy import Column, String, Integer
from qg.db.models import HasIdMixin
from itdblib.models import base


class Model(base.BASE, HasIdMixin):

    __tablename__ = "mp_model"

    provider_id = Column(Integer)
    name = Column(String)
