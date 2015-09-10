# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import basedal
from qg.core import log as logging
from itdblib.models.mp_model import Model
from sqlalchemy import func
from sqlalchemy.sql import and_
LOG = logging.getLogger(__name__)


class ModelDal(basedal.BaseDal):
    def __init__(self):
        self.session = self._getSession()

    def get_model_all(self):
        return self.session.query(Model).all()

    def get_model_by_prov_id(self, prov_id):
        return self.session.query(Model).filter(
                Model.provider_id == prov_id).all()

    def add_model(self, provider_id, name):
        model = Model()
        model.provider_id = provider_id
        model.name = name
        self.begin()
        self.session.add(model)
        self.commit()

    def del_model_by_id(self, id):
        try:
            model = self.session.query(Model).filter(Model.id == id).first()
            self.session.delete(model)
            self.commit()
        except Exception as e:
            LOG.error('del_model_by_id error:%s' % str(e))

    def get_model_by_pd_ch(self, prov_id, ch_name):
        try:
            return self.session.query(Model).filter(and_
                            (Model.provider_id == prov_id),
                            (func.lower(Model.name)
                             == func.lower(ch_name))).first()
        except Exception as e:
            LOG.error('get_model_by_pd_ch error:%s' % str(e))
            return None

    def get_model_name_by_id(self, model_id):
        try:
            return self.session.query(Model).filter(
                            Model.id == model_id).first()
        except Exception as e:
            LOG.error('get_model_name_by_id error:%s' % str(e))
            return None

    def get_model_list_by_prov_id(self, prov_id):
        try:
            modelInfos = self.session.query(Model).filter(
                            Model.provider_id == prov_id).all()
            modelList = set()
            for modelInfo in modelInfos:
                modelList.add(modelInfo.id)
            return modelList
        except Exception as e:
            LOG.error('get_model_name_by_id error:%s' % str(e))
            return []