# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import basedal
from qg.core import log as logging
from itdblib.common.time_utils import get_now_date
from itdblib.models.tb_asset_phone_info import AssetPhoneInfoModel
from itdblib.common.asset_tool_utils import judge_key_not_null
from sqlalchemy.sql import and_, or_
from sqlalchemy import func
from itdblib.db.api import get_engine
from sqlalchemy.sql import table, column
from sqlalchemy import func

LOG = logging.getLogger(__name__)


class AssetPhoneInfoDal(basedal.BaseDal):
    def __init__(self):
        self.session = self._getSession()

    def get_asset_phone_info_all(self):
        return self.session.query(AssetPhoneInfoModel).all()

    def get_asset_phone_info_limit(self, start, count):
        return self.session.query(AssetPhoneInfoModel).offset(start).limit(count)

    def get_asset_phone_info_num(self):
        return self.session.query(AssetPhoneInfoModel).count()

    def store_new_phone_data(self, data):
        try:
            self.begin()
            assetPhoneInfo = self.add_new_asset_phone_model(data)
            assetPhoneInfo.update_time = get_now_date()
            self.session.add(assetPhoneInfo)
            self.commit()
            return True, u'添加电话号码成功！'
        except Exception as _ex:
            error_msg = "error occured while store_new_phone_data: %s" % str(_ex)
            LOG.error(error_msg)
            return False, u'添加电话号码失败！'

    def add_new_asset_phone_model(self, data):
        assetPhoneInfo = AssetPhoneInfoModel()
        assetPhoneInfo.remark = data["remark"]
        assetPhoneInfo.user_name = data["user_name"]
        assetPhoneInfo.asset_type_id = data["asset_type"]
        assetPhoneInfo.store_place_id = data["store_place"]
        assetPhoneInfo.device_state_id = data['device_state']
        assetPhoneInfo.store_state_id = data['store_state']
        assetPhoneInfo.in_out_reason_id = data['in_out_reason']
        assetPhoneInfo.phone_no = data['phone_no']
        assetPhoneInfo.update_time = get_now_date()
        return assetPhoneInfo

    def get_asset_phone_info_by_search_val_all(self, id, start, count):
        model = self.get_phone_asset_info_sql(id)
        return model.offset(start).limit(count)

    def get_asset_phone_info_excel_by_search_val_all(self, id):
        model = self.get_phone_asset_info_sql(id)
        return model.all()

    def get_asset_phone_info_query_num(self, id):
        model = self.get_phone_asset_info_sql(id)
        return model.count()

    def get_phone_asset_info_sql(self, in_id):
        in_id = str(in_id).lower()
        in_id = in_id.replace('%', '\%') + '%'
        model = self.session.query(AssetPhoneInfoModel). \
            filter(or_(func.lower(AssetPhoneInfoModel.phone_no).like(in_id),
                       func.lower(AssetPhoneInfoModel.user_name).like(in_id)
        )
        )
        return model

    def get_phone_asset_info_by_phone_no(self, phone):
        return self.session.query(AssetPhoneInfoModel). \
            filter(AssetPhoneInfoModel.phone_no == phone).first()

    def get_asset_phone_info_by_search_val_one(self, id):
        model = self.get_phone_asset_info_sql(id)
        return model.first()

    def get_advanced_phone_search_val(self, params):
        model = self.session.query(AssetPhoneInfoModel)
        if judge_key_not_null(params, "store_state"):
            model = model.filter(AssetPhoneInfoModel.store_state_id == params['store_state'])
        if judge_key_not_null(params, "device_state"):
            model = model.filter(AssetPhoneInfoModel.device_state_id == params['device_state'])
        if judge_key_not_null(params, "store_place"):
            model = model.filter(AssetPhoneInfoModel.store_place_id == params['store_place'])
        if judge_key_not_null(params, "in_out_reason"):
            model = model.filter(AssetPhoneInfoModel.in_out_reason_id == params['in_out_reason'])
        if judge_key_not_null(params, "asset_type"):
            model = model.filter(AssetPhoneInfoModel.asset_type_id == params['asset_type'])
        if judge_key_not_null(params, "date_from1"):
            model = model.filter(AssetPhoneInfoModel.up_time >= params['date_from1'])
        if judge_key_not_null(params, "date_to1"):
            model = model.filter(AssetPhoneInfoModel.up_time <= params['date_to1'])
        if judge_key_not_null(params, "date_from2"):
            model = model.filter(AssetPhoneInfoModel.update_time >= params['date_from2'])
        if judge_key_not_null(params, "date_to2"):
            model = model.filter(AssetPhoneInfoModel.update_time <= params['date_to2'])
        if judge_key_not_null(params, "asset_id_list"):
            model = model.filter(AssetPhoneInfoModel.phone_no.in_(params["asset_id_list"]))
        return model

    def get_advanced_phone_search_val_limit(self, params, start, count):
        return self.get_advanced_phone_search_val(params).offset(start).limit(count)

    def get_advanced_phone_search_val_count(self, params):
        return self.get_advanced_phone_search_val(params).count()

    def update_asset_phone_info_by_id(self, data):
        try:
            self.begin()
            assetInfoModel = self.get_phone_asset_info_sql(data['phone_no']).first()
            print assetInfoModel.asset_type_id
            if assetInfoModel is not None:
                assetInfoModel.device_state_id = data['device_state']
                assetInfoModel.store_place_id = data['store_place']
                assetInfoModel.store_state_id = data['store_state']
                assetInfoModel.in_out_reason_id = data['in_out_reason']
                assetInfoModel.remark = data['remark']
                assetInfoModel.user_name = data['user_name']
                assetInfoModel.update_time = get_now_date()
                self.commit()
            return True, u'添加电话号码成功！'
        except Exception, _ex:
            LOG.error('update_asset_phone_info_by_id error[%s]', str(_ex))
            return False, u'添加电话号码失败！'

    def get_phone_out_data(self, data):
        try:
            return self.session.query(AssetPhoneInfoModel). \
                       filter(and_(AssetPhoneInfoModel.device_state_id == data['device_state'],
                                   AssetPhoneInfoModel.store_place_id == data['store_place'],
                                   AssetPhoneInfoModel.store_state_id == data['store_state'],
                                   AssetPhoneInfoModel.asset_type_id == data['asset_type'])
            ).all(), 'get_phone_out_data succeed!'
        except Exception, _ex:
            LOG.error('get_phone_out_data error[%s]', str(_ex))
            return None, 'get_phone_out_data failed!'

    def update_asset_phone_info_out(self, data):
        try:
            self.begin()
            print data
            print data['remark']
            assetInfoModel = self.get_phone_asset_info_sql(data['phone_no']).first()
            if assetInfoModel is not None:
                assetInfoModel.store_place_id = data['store_place']
                assetInfoModel.in_out_reason_id = data['in_out_reason']
                assetInfoModel.remark = data['remark']
                assetInfoModel.store_state_id = data['store_state']
                assetInfoModel.user_name = ''
                assetInfoModel.update_time = get_now_date()
                self.commit()
            return True, u'已有电话号码出库成功！'
        except Exception, _ex:
            LOG.error('update_asset_phone_info_out error[%s]', str(_ex))
            return False, u'已有电话号码出库失败！'

    def get_advanced_search_val_all_datas(self, params):
        return self.get_advanced_phone_search_val(params).all()

    def get_asset_info_excel_by_search_val_all(self, id):
        model = self.get_phone_asset_info_sql(id)
        return model.all()

    def add_batch_asset_phone_infos(self, datas):
        try:
            engine = get_engine()
            connection = engine.connect()
            trans = connection.begin()
            # 得到tb_asset_info这个表
            aim = table(
                "tb_asset_phone_info",
                column("phone_no"),
                column("asset_type_id"),
                column("device_state_id"),
                column("user_name"),
                column("store_place_id"),
                column("remark"),
                column("in_out_reason_id"),
                column("store_state_id"),
                column("up_time"),
                column("create_time"),
                column("update_time"),
            )
            ins = aim.insert()
            connection.execute(ins, datas)
            trans.commit()
        except Exception, _ex:
            msg = "add_batch_asset_phone_infos error: %s" % str(_ex)
            LOG.error(msg)
            return False, u'批量添加数据失败！'
        finally:
            connection.close()
        return True, u'批量添加数据成功！'