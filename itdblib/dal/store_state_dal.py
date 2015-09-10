# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import basedal
from qg.core import log as logging
from itdblib.models.dt_store_state import StoreState
LOG = logging.getLogger(__name__)


class StoreStateDal(basedal.BaseDal):
    def __init__(self):
        self.session = self._getSession()

    def get_store_state_all(self):
        return self.session.query(StoreState).all()

    def add_asset_type(self, store_state):
        storeState = StoreState()
        storeState.ch_name = store_state
        self.session.add(storeState)
        self.commit()

    def get_store_state_id_by_ch_name(self, ch_name):
        try:
            return self.session.query(StoreState).filter(
                    StoreState.ch_name == ch_name).first()
        except Exception as e:
            LOG.error('get_store_state_id_by_ch_name error:%s' % str(e))
            return None

    def get_store_state_name_by_id(self, store_state_id):
        try:
            return self.session.query(StoreState).filter(
                    StoreState.id == store_state_id).first()
        except Exception as e:
            LOG.error('get_store_state_name_by_id error:%s' % str(e))
            return None

    def del_store_state_by_ch_name(self, store_state):
        self.begin()
        try:
            storeState = self.session.query(StoreState).\
                            filter(StoreState.ch_name == store_state).\
                            first()
            if storeState is not None:
                self.session.delete(storeState)
                self.commit()
            return True
        except Exception, _ex:
            LOG.error('del_store_state_by_ch_name error:%s' % str(_ex))
