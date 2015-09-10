# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import basedal
from qg.core import log as logging
from itdblib.models.dt_store_place import StorePlace
LOG = logging.getLogger(__name__)


class StorePlaceDal(basedal.BaseDal):
    def __init__(self):
        self.session = self._getSession()

    def get_store_place_all(self):
        return self.session.query(StorePlace).all()

    def add_store_place(self, ch_name, admin_name):
        self.begin()
        storePlace = StorePlace()
        storePlace.ch_name = ch_name
        storePlace.admin_name = admin_name
        self.session.add(storePlace)
        self.commit()

    def get_store_place_id_by_ch_name(self, ch_name):
        try:
            return self.session.query(StorePlace).filter(
                        StorePlace.ch_name == ch_name).first()
        except Exception as e:
            LOG.error('get_store_place_id_by_ch_name error:%s' % str(e))
            return None

    def get_store_place_name_by_id(self, store_place_id):
        try:
            return self.session.query(StorePlace).filter(
                        StorePlace.id == store_place_id).first()
        except Exception as e:
            LOG.error('get_store_place_name_by_id error:%s' % str(e))
            return None

    def get_admin_name_by_ch_name(self, ch_name):
        try:
            return self.session.query(StorePlace).filter(
                        StorePlace.ch_name == ch_name).first()
        except Exception as e:
            LOG.error('get_store_place_id_by_ch_name error:%s' % str(e))
            return None

    def del_store_place_by_ch_name(self, ch_name):
        self.begin()
        try:
            storePlace = self.session.query(StorePlace).\
                            filter(StorePlace.ch_name == ch_name).\
                            first()
            if storePlace is not None:
                self.session.delete(storePlace)
                self.commit()
            return True
        except Exception, _ex:
            LOG.error('del_store_place_by_ch_name error:%s' % str(_ex))
