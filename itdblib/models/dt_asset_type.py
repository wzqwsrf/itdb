# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from sqlalchemy import Column, String
from qg.db.models import HasIdMixin
from itdblib.models import base
from itdblib.models.sqltypes import LTree


class AssetTypeModel(base.BASE, HasIdMixin):

    __tablename__ = 'dt_asset_type'

    ch_name = Column(String(20))
    asset_path = Column(LTree(), nullable=False, unique=True)
