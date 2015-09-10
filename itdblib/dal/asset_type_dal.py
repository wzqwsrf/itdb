# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import basedal
from qg.core import log as logging
from itdblib.models.dt_asset_type import AssetTypeModel
from sqlalchemy import exc as sa_exc
from sqlalchemy.sql.expression import text
from sqlalchemy import func
from sqlalchemy.sql import or_
LOG = logging.getLogger(__name__)


class AssetTypeDal(basedal.BaseDal):
    def __init__(self):
        self.session = self._getSession()

    def get_asset_type_all(self):
        return self.session.query(AssetTypeModel).all()

    def search_by_path(self, lquery):
        unbind = text('asset_path ~ :lquery')
        bound = unbind.bindparams(lquery=lquery)
        node_query = self.session.query(AssetTypeModel).filter(bound)
        return node_query.all()

    def get_asset_type_id_by_ch_name(self, ch_name):
        return self.session.query(AssetTypeModel) \
            .filter(func.lower(AssetTypeModel.ch_name) == func.lower(ch_name)) \
            .first()

    def get_asset_type_name_by_id(self, asset_type_id):
        return self.session.query(AssetTypeModel) \
            .filter(AssetTypeModel.id == asset_type_id) \
            .first()

    def get_asset_type_by_name_or_path(self, ch_name, path):
        return self.session.query(AssetTypeModel).filter(or_(
                    func.lower(AssetTypeModel.ch_name) == func.lower(ch_name),
                    AssetTypeModel.asset_path == path
                )).first()

    def add_asset_type(self, ch_name, path):
        self.begin()
        assetTypeModel = AssetTypeModel()
        assetTypeModel.ch_name = ch_name
        assetTypeModel.asset_path = path
        self.session.add(assetTypeModel)
        self.commit()

    def del_asset_type_by_ch_name(self, ch_name):
        self.begin()
        try:
            assetTypeModel = self.session.query(AssetTypeModel). \
                filter(func.lower(AssetTypeModel.ch_name) == func.lower(ch_name)). \
                first()
            if assetTypeModel is not None:
                self.session.delete(assetTypeModel)
                self.commit()
            return True
        except Exception as _ex:
            LOG.error('del_asset_type_by_ch_name error:%s' % str(_ex))
