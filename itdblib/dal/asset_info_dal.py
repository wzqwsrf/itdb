# -*- coding: utf-8 -*-
#
# Copyright @ 2014 OPS, Qunar Inc. (qunar.com)
#
# Author: zhenqing.wang <zhenqing.wang@qunar.com>
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import basedal
from qg.core import log as logging
from itdblib.models.tb_asset_info import AssetInfoModel
from itdblib.common.time_utils import get_now_date
from itdblib.common.asset_tool_utils import judge_key_not_null
from sqlalchemy.sql import or_
from itdblib.db.api import get_engine
from sqlalchemy.sql import table, column
from sqlalchemy import func

LOG = logging.getLogger(__name__)


class AssetInfoDal(basedal.BaseDal):
    def __init__(self):
        self.session = self._getSession()

    def get_asset_info_all(self):
        return self.session.query(AssetInfoModel).all()

    def get_asset_info_limit(self, start, count):
        return self.session.query(AssetInfoModel).offset(start).limit(count)

    def get_asset_info_num(self):
        return self.session.query(AssetInfoModel).count()

    def get_asset_info_by_id(self, asset_id):
        return self.session.query(AssetInfoModel). \
            filter(func.lower(AssetInfoModel.asset_id)
                   == func.lower(asset_id)).first()

    def get_asset_info_first_by_id(self, asset_id):
        asset_id = str(asset_id).lower()
        asset_id = asset_id.replace('%', '\%') + '%'
        return self.session.query(AssetInfoModel). \
            filter(func.lower(AssetInfoModel.asset_id).like(asset_id)).limit(5)

    def get_asset_info_by_user_name(self, rtx_id):
        return self.session.query(AssetInfoModel). \
            filter(func.lower(AssetInfoModel.user_name)
                   == func.lower(rtx_id)).all()

    def get_asset_info_by_sn(self, sn):
        return self.session.query(AssetInfoModel). \
            filter(func.lower(AssetInfoModel.sn) == func.lower(sn)). \
            first()

    def get_asset_info_by_mac(self, mac):
        mac = str(mac).lower()
        mac = mac.replace('%', '\%') + '%'
        return self.session.query(AssetInfoModel). \
            filter(
            func.lower(AssetInfoModel.type_info['mac']).like(mac),
            # func.lower(AssetInfoModel.type_info['imei']).like(id + "%")
        ).first()

    def get_asset_info_by_imei(self, imei):
        imei = str(imei).lower()
        imei = imei.replace('%', '\%') + '%'
        return self.session.query(AssetInfoModel). \
            filter(
            func.lower(AssetInfoModel.type_info['imei']).like(imei)
        ).first()


    def get_asset_info_by_search_val_one(self, id):
        model = self.get_asset_info_sql(id)
        return model.first()

    def get_asset_info_by_search_val_all(self, id, start, count):
        model = self.get_asset_info_sql(id)
        return model.offset(start).limit(count)

    def get_asset_info_excel_by_search_val_all(self, id):
        model = self.get_asset_info_sql(id)
        return model.all()

    def get_asset_info_query_num(self, id):
        model = self.get_asset_info_sql(id)
        return model.count()

    def get_asset_info_sql(self, in_id):
        in_id = str(in_id).lower()
        in_id = in_id.replace('%', '\%') + '%'
        model = self.session.query(AssetInfoModel). \
            filter(or_(func.lower(AssetInfoModel.asset_id).like(in_id),
                       func.lower(AssetInfoModel.user_name).like(in_id),
                       func.lower(AssetInfoModel.sn).like(in_id),
                       func.lower(AssetInfoModel.type_info['mac']).like(in_id),
                       func.lower(AssetInfoModel.type_info['imei']).like(in_id)
        )
        )
        return model

    def get_asset_info_by_all_unique(self, id):
        id = func.lower(id)
        return self.session.query(AssetInfoModel). \
            filter(or_(func.lower(AssetInfoModel.sn) == id,
                       func.lower(AssetInfoModel.type_info['mac']) == id,
                       func.lower(AssetInfoModel.type_info['imei']) == id
        )
        ).first()

    def update_asset_info_by_id(self, data):
        try:
            self.begin()
            assetInfoModel = self.get_asset_info_by_id(data['asset_id'])
            if assetInfoModel is not None:
                assetInfoModel.device_state_id = data['device_state']
                assetInfoModel.store_place_id = data['store_place']
                assetInfoModel.store_state_id = data['store_state']
                assetInfoModel.in_out_reason_id = data['in_out_reason']
                assetInfoModel.remark = data['remark']
                assetInfoModel.user_name = data['user_name']
                assetInfoModel.update_time = get_now_date()
                self.commit()
            return True, u'变更已有库存数据成功，资产编号为' + data['asset_id']
        except Exception, _ex:
            LOG.error('update_asset_info_by_id error[%s]', str(_ex))
            return False, u'变更已有库存数据失败，资产编号为' + data['asset_id']

    def edit_asset_info(self, data):
        try:
            self.begin()
            asset_id = data['asset_id']
            assetInfoModel = self.get_asset_info_by_id(asset_id)
            if assetInfoModel is not None:
                self.add_value_to_info(assetInfoModel, data)
                self.commit()
            return True, 'edit_asset_info success'
        except Exception as e:
            LOG.error('edit_asset_info error: %s', str(e))
            return False, 'edit_asset_info failed'

    def add_new_asset_info(self, data):
        try:
            self.begin()
            asset_info_model = AssetInfoModel()
            self.add_value_to_info(asset_info_model, data)
            asset_info_model.asset_id = str(data['asset_id']).upper()
            asset_info_model.up_time = get_now_date()
            asset_info_model.create_time = get_now_date()
            self.session.add(asset_info_model)
            self.commit()
            return True, u'添加固定资产成功！'
        except Exception as e:
            error_msg = 'add_new_asset_info error: %s', str(e)
            LOG.error(error_msg)
            return False, u'添加固定资产失败！'

    def add_asset_info(self, assetInfoModel):
        assetInfoModel.create_time = get_now_date()
        assetInfoModel.update_time = get_now_date()
        self.session.add(assetInfoModel)

    def add_value_to_info(self, asset_info_model, data):
        asset_info_model.asset_type_id = data['asset_type']
        asset_info_model.model_id = data['model']
        value = str(data['sn'])
        if value:
            value = value.upper()
        asset_info_model.sn = value
        asset_info_model.user_name = str(data['user_name']).lower()
        asset_info_model.store_place_id = data['store_place']
        asset_info_model.store_state_id = data['store_state']
        asset_info_model.device_state_id = data['device_state']
        asset_info_model.in_out_reason_id = data['in_out_reason']
        asset_info_model.update_time = get_now_date()
        asset_info_model.remark = data['remark']
        asset_info_model.type_info = data['type_info']
        return asset_info_model

    def add_batch_asset_infos(self, datas):
        print datas
        try:
            engine = get_engine()
            connection = engine.connect()
            trans = connection.begin()
            # 得到tb_asset_info这个表
            aim = table(
                "tb_asset_info",
                column("asset_id"),
                column("asset_type_id"),
                column("model_id"),
                column("device_state_id"),
                column("user_name"),
                column("store_place_id"),
                column("remark"),
                column("in_out_reason_id"),
                column("sn"),
                column("store_state_id"),
                column("up_time"),
                column("create_time"),
                column("update_time"),
                column("type_info"),
            )
            ins = aim.insert()
            connection.execute(ins, datas)
            trans.commit()
        except Exception, _ex:
            msg = "add_batch_asset_infos error: %s" % str(_ex)
            LOG.error(msg)
            return False, u'批量添加数据失败！'
        finally:
            connection.close()
        return True, u'批量添加数据成功！'

    def get_advanced_search_val(self, params):
        print params
        model = self.session.query(AssetInfoModel)
        if judge_key_not_null(params, "store_state"):
            model = model.filter(AssetInfoModel.store_state_id == params['store_state'])
        if judge_key_not_null(params, "device_state"):
            model = model.filter(AssetInfoModel.device_state_id == params['device_state'])
        if judge_key_not_null(params, "store_place"):
            model = model.filter(AssetInfoModel.store_place_id == params['store_place'])
        if judge_key_not_null(params, "in_out_reason"):
            model = model.filter(AssetInfoModel.in_out_reason_id == params['in_out_reason'])
        if judge_key_not_null(params, "asset_type"):
            model = model.filter(AssetInfoModel.asset_type_id == params['asset_type'])
        if judge_key_not_null(params, "provider"):
            if judge_key_not_null(params, "model"):
                model = model.filter(AssetInfoModel.model_id == params['model'])
            else:
                model = model.filter(AssetInfoModel.model_id.in_(params["model_list"]))
        if judge_key_not_null(params, "date_from1"):
            model = model.filter(AssetInfoModel.up_time >= params['date_from1'])
        if judge_key_not_null(params, "date_to1"):
            model = model.filter(AssetInfoModel.up_time <= params['date_to1'])
        if judge_key_not_null(params, "date_from2"):
            model = model.filter(AssetInfoModel.update_time >= params['date_from2'])
        if judge_key_not_null(params, "date_to2"):
            model = model.filter(AssetInfoModel.update_time <= params['date_to2'])
        if judge_key_not_null(params, "asset_id_list"):
            model = model.filter(AssetInfoModel.asset_id.in_(params["asset_id_list"]))
        return model

    def get_advanced_search_val_limit(self, params, start, count):
        return self.get_advanced_search_val(params).offset(start).limit(count)

    def get_advanced_search_val_count(self, params):
        return self.get_advanced_search_val(params).count()

    def get_advanced_search_val_all_datas(self, params):
        return self.get_advanced_search_val(params).all()
