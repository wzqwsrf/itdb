# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import basedal
from qg.core import log as logging
from sqlalchemy import and_
from itdblib.models.mp_provider import Provider
from sqlalchemy import func
LOG = logging.getLogger(__name__)


class ProviderDal(basedal.BaseDal):

    def __init__(self):
        self.session = self._getSession()

    def get_provider_all(self):
        return self.session.query(Provider).all()

    def get_prov_by_asset_type(self, asset_type_id):
        prov_list = self.session.query(Provider)\
                .filter_by(asset_type_id=asset_type_id)\
                .all()
        provs = set()
        for prov in prov_list:
            provs.add(prov.name)
        return list(provs)

    def get_prov_by_id_and_at(self, asset_type_id, provider):
        try:
            return self.session.query(Provider)\
                .filter(and_(func.lower(Provider.name) == func.lower(provider),
                            Provider.asset_type_id == asset_type_id))\
                .first()
        except Exception as e:
            LOG.error('get_prov_by_id_and_at error:%s' % str(e))
            return None

    def get_prov_name_by_atd_md(self, asset_type_id, prov_id):
        try:
            return self.session.query(Provider)\
                .filter(and_(Provider.id == prov_id,
                            Provider.asset_type_id == asset_type_id))\
                .first()
        except Exception as e:
            LOG.error('get_prov_name_by_atd_md error:%s' % str(e))
            return None

    def add_new_provider(self, asset_type_id, name, ch_name):
        provider = Provider()
        provider.asset_type_id = asset_type_id
        provider.name = name
        provider.ch_name = ch_name
        self.begin()
        self.session.add(provider)
        self.commit()

    def del_provider_by_id(self, id):
        try:
            provider = self.session.query(Provider).filter(
                        Provider.id == id).first()
            self.session.delete(provider)
            self.commit()
        except Exception as e:
            LOG.error('del_provider_by_id error[%s]', str(e))
