# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>



from sqlalchemy import Column, String
from qg.db.models import HasIdMixin
from itdblib.models import base


class StorePlace(base.BASE, HasIdMixin):

    __tablename__ = "dt_store_place"

    ch_name = Column(String)
    admin_name = Column(String)
