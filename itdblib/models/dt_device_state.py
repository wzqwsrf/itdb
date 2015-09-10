# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from sqlalchemy import Column, String
from qg.db.models import HasIdMixin
from itdblib.models import base


class DeviceState(base.BASE, HasIdMixin):

    __tablename__ = "dt_device_state"

    ch_name = Column(String(15))
