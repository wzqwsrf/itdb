# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


import basedal
from itdblib.models.tb_operation_info import OperationInfo
from qg.core import log as logging
from itdblib.db.api import get_engine
from sqlalchemy.sql import table, column
from sqlalchemy import func

LOG = logging.getLogger(__name__)


class OperationInfoDal(basedal.BaseDal):
    def __init__(self):
        self.session = self._getSession()

    def get_all_oper_infos(self):
        """ query all operation infos
        """
        operInfos = self.session.query(OperationInfo). \
            order_by(OperationInfo.oper_time.desc()).all()
        return operInfos

    def get_oper_info_by_asset_id(self, assetId):
        """ according to assetId query operation infos
        """
        operInfo = self.get_model_by_asset_id(assetId).first()
        return operInfo

    def get_all_oper_info_by_asset_id(self, assetId):
        """ according to assetId query operation infos
        """
        operInfos = self.get_model_by_asset_id(assetId).all()
        return operInfos

    def get_model_by_asset_id(self, assetId):
        return self.session.query(OperationInfo).filter(
            func.lower(OperationInfo.asset_id) ==
            func.lower(assetId)).order_by(
            OperationInfo.oper_time.desc())

    def get_asset_id_list_by_operator(self, oper_name):
        operInfos = self.session.query(OperationInfo).filter(
            OperationInfo.operator == oper_name).all()
        assetList = set()
        for operInfo in operInfos:
            assetList.add(operInfo.asset_id)
        return assetList

    def add_oper_infos(self, assetId, type,
                       operator, text, before_field, after_field):
        """ according to assetId add operation infos
        """
        try:
            self.begin()
            ops = OperationInfo()
            ops.asset_id = assetId
            ops.oper_type = type
            ops.operator = operator
            ops.text = text
            ops.before_field = before_field
            ops.after_field = after_field
            self.session.add(ops)
            self.commit()
        except Exception, _ex:
            LOG.error("add_oper_infos error: %s" % str(_ex))
            return False
        return True

    def add_batch_oper_infos(self, datas):
        print datas
        try:
            engine = get_engine()
            connection = engine.connect()
            trans = connection.begin()
            # 得到tb_asset_info这个表
            aim = table(
                "tb_operation_info",
                column("asset_id"),
                column("oper_time"),
                column("oper_type"),
                column("operator"),
                column("text"),
                column("before_field"),
                column("after_field"),
            )
            ins = aim.insert()
            connection.execute(ins, datas)
            trans.commit()
        except Exception, _ex:
            msg = "add_batch_oper_infos error: %s" % str(_ex)
            LOG.error(msg)
            return False, msg
        finally:
            connection.close()
        return True, 'add_batch_oper_infos succeed'