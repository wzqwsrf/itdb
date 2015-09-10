# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import basedal
from qg.core import log as logging
from itdblib.models.dt_in_out_reason import InOutReason
from sqlalchemy import func
LOG = logging.getLogger(__name__)


class InOutReasonDal(basedal.BaseDal):

    def __init__(self):
        self.session = self._getSession()

    def get_in_out_reason_all(self):
        return self.session.query(InOutReason).all()

    def get_in_reason_all(self):
        q = self.session.query(InOutReason)\
            .filter(InOutReason.in_or_out == 'IN_REASON')
        return q.all()

    def get_out_reason_all(self):
        q = self.session.query(InOutReason)\
            .filter(InOutReason.in_or_out == 'OUT_REASON')
        return q.all()

    def get_reason_id_by_ch_name(self, ch_name):
        try:
            return self.session.query(InOutReason).filter(
                        func.lower(InOutReason.ch_name)
                        == func.lower(ch_name)).first()
        except Exception as e:
            LOG.error('get_reason_id_by_ch_name error:%s' % str(e))
            return None

    def get_reason_name_by_id(self, in_out_reason_id):
        try:
            return self.session.query(InOutReason).filter(
                        InOutReason.id == in_out_reason_id).first()
        except Exception as e:
            LOG.error('get_reason_name_by_id error:%s' % str(e))
            return None