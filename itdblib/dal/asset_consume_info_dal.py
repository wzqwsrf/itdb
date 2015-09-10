# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import basedal
from qg.core import log as logging
from itdblib.common.time_utils import get_now_date
from itdblib.models.tb_asset_consume_info import AssetConsumeInfoModel
from itdblib.common.asset_tool_utils import judge_key_not_null
from sqlalchemy.sql import and_
from sqlalchemy import func

LOG = logging.getLogger(__name__)


class AssetConsumeInfoDal(basedal.BaseDal):
    def __init__(self):
        self.session = self._getSession()

    def get_asset_consume_info_all(self):
        return self.session.query(AssetConsumeInfoModel).all()

    def get_asset_consume_info_limit(self, start, count):
        return self.session.query(AssetConsumeInfoModel).offset(start).limit(count)

    def get_asset_consume_info_num(self):
        return self.session.query(AssetConsumeInfoModel).count()

    def get_asset_type_model_place_num(self, asset_type,
                                       model_id, store_place_id):
        return self.get_actual_asset_by_type_model_place(
            asset_type,
            model_id,
            store_place_id,
            1)

    def get_asset_type_model_user_name_num(self, asset_type,
                                           model_id, user_name, store_state):
        return self.session.query(AssetConsumeInfoModel).filter(
            and_(AssetConsumeInfoModel.asset_type_id == asset_type,
                 AssetConsumeInfoModel.model_id == model_id,
                 AssetConsumeInfoModel.store_state_id == store_state,
                 func.lower(AssetConsumeInfoModel.user_name) == func.lower(user_name))).first()

    def get_asset_consume_info_by_search_val_all(self, id, start, count):
        model = self.get_consume_asset_info_sql(id)
        return model.offset(start).limit(count)

    def get_asset_consume_info_query_num(self, id):
        model = self.get_consume_asset_info_sql(id)
        return model.count()

    def store_new_consume_data(self, data):
        try:
            self.begin()
            assetConsumeInfo = self.get_actual_asset_by_type_model_place(
                data["asset_type"],
                data["model"],
                data["store_place"],
                1)
            if assetConsumeInfo:
                assetConsumeInfo.in_num = data["in_num"]
                assetConsumeInfo.remark = data["remark"]
                assetConsumeInfo.user_name = data["user_name"]
                assetConsumeInfo.update_time = get_now_date()
                self.commit()
            else:
                assetConsumeInfo = self.add_new_asset_consume_model(
                    data, 1, data["in_num2"])
                self.session.add(assetConsumeInfo)
                self.commit()
            return True, assetConsumeInfo.id
        except Exception as _ex:
            error_msg = "error occured while store_new_consume_data: %s" % str(_ex)
            LOG.error(error_msg)
            return False, -1

    def get_actual_asset_by_type_model_place(self, asset_type,
                                             model_id, store_place_id,
                                             store_state):
        return self.session.query(AssetConsumeInfoModel). \
            filter(and_(AssetConsumeInfoModel.asset_type_id == asset_type,
                        AssetConsumeInfoModel.model_id == model_id,
                        AssetConsumeInfoModel.store_place_id == store_place_id,
                        AssetConsumeInfoModel.store_state_id == store_state,
                        AssetConsumeInfoModel.device_state_id == 1)). \
            first()

    def store_old_consume_data(self, data):
        try:
            # 从哪个库出
            assetConsumeInfo = self.get_actual_asset_by_type_model_place(
                data["asset_type"],
                data["model"],
                data["store_place1"],
                1)
            if assetConsumeInfo:
                self.begin()
                assetConsumeInfo.in_num -= int(data["out_num"])
                assetConsumeInfo.out_num += int(data["out_num"])
                assetConsumeInfo.update_time = get_now_date()
                self.commit()
            info = None
            if data['usage'] == '办公':
                # info = self.get_actual_asset_by_type_model_place(
                #     data["asset_type"],
                #     data["model"],
                #     data["store_place2"],
                #     2)
                data['store_state'] = 2
            else:
                info = self.get_actual_asset_by_type_model_place(
                    data["asset_type"],
                    data["model"],
                    data["store_place2"],
                    1)
                data['store_state'] = 1
            if info:
                self.begin()
                assetConsumeInfo.in_num += int(data["out_num"])
                assetConsumeInfo.update_time = get_now_date()
                self.commit()
            else:
                data['store_place'] = data['store_place2']
                data['device_state'] = 1
                newInfo = self.add_new_asset_consume_model(data, data['store_state'], data['out_num'])
                self.begin()
                self.session.add(newInfo)
                self.commit()
            return True
        except Exception as _ex:
            LOG.error("error occured while store_old_consume_data: %s" % str(_ex))
            return False

    def add_new_asset_consume_model(self, data, store_state, consume_num):
        assetConsumeInfo = AssetConsumeInfoModel()
        assetConsumeInfo.in_num = int(consume_num)
        assetConsumeInfo.remark = data["remark"]
        assetConsumeInfo.user_name = data["user_name"]
        assetConsumeInfo.asset_type_id = data["asset_type"]
        assetConsumeInfo.model_id = data["model"]
        assetConsumeInfo.store_place_id = data["store_place"]
        assetConsumeInfo.device_state_id = data['device_state']
        assetConsumeInfo.in_out_reason_id = data['in_out_reason']
        assetConsumeInfo.store_state_id = store_state
        assetConsumeInfo.update_time = get_now_date()
        assetConsumeInfo.out_num = 0
        return assetConsumeInfo

    def get_asset_consume_info_by_search_val_one(self, id):
        model = self.get_consume_asset_info_sql(id)
        return model.first()

    def get_consume_asset_info_sql(self, id):
        id = str(id).lower()
        id = id.replace('%', '\%') + '%'
        model = self.session.query(AssetConsumeInfoModel). \
            filter(
            func.lower(AssetConsumeInfoModel.user_name).like(id)
        )
        return model

    def get_consume_asset_info_by_id(self, id):
        return self.session.query(AssetConsumeInfoModel). \
            filter(AssetConsumeInfoModel.id == id).first()

    def update_asset_consume_info_by_id(self, data):
        try:
            self.begin()
            assetInfoModel = self.get_consume_asset_info_sql(data['user_name']).first()
            if assetInfoModel is not None:
                assetInfoModel.device_state_id = data['device_state']
                assetInfoModel.store_place_id = data['store_place']
                assetInfoModel.store_state_id = data['store_state']
                assetInfoModel.in_out_reason_id = data['in_out_reason']
                assetInfoModel.remark = data['remark']
                assetInfoModel.user_name = data['user_name']
                assetInfoModel.update_time = get_now_date()
                self.commit()
            return True, 'update consume_info succeed!'
        except Exception, _ex:
            LOG.error('update_asset_consume_info_by_id error[%s]', str(_ex))
            return False, 'update consume_info failed!'

    def store_old_consume_in_data(self, data):
        try:
            self.begin()
            assetConsumeInfo = self.get_actual_asset_by_type_model_place(
                data["asset_type"],
                data["model"],
                data["store_place"],
                1)
            if assetConsumeInfo:
                assetConsumeInfo.in_num += int(data["c_in_num"])
                assetConsumeInfo.remark = data["remark"]
                assetConsumeInfo.update_time = get_now_date()
                self.commit()
            else:
                assetConsumeInfo = self.add_new_asset_consume_model(
                    data, 1, data["c_in_num"])
                self.session.add(assetConsumeInfo)
                self.commit()
            self.begin()
            assetInfo = self.get_asset_type_model_user_name_num(data["asset_type"], data["model"],
                                                                data["old_user_name"], 2)
            if data["c_in_num"] == data["in_num_c"]:  # 全部回收，直接删掉。
                if assetInfo is not None:
                    self.session.delete(assetInfo)
                    self.commit()
            else:
                assetInfo.in_num -= int(data["c_in_num"])
                assetInfo.out_num += int(data["c_in_num"])
                assetInfo.update_time = get_now_date()
                self.commit()

            return True, assetConsumeInfo.id
        except Exception as _ex:
            error_msg = "error occured while store_old_consume_in_data: %s" % str(_ex)
            LOG.error(error_msg)
            return False, -1

    def get_advanced_consume_search_val_limit(self, params, start, count):
        return self.get_advanced_consume_search_val(params).offset(start).limit(count)

    def get_advanced_consume_search_val_count(self, params):
        return self.get_advanced_consume_search_val(params).count()

    def get_advanced_consume_search_val(self, params):
        print params['model_list']
        model = self.session.query(AssetConsumeInfoModel)
        if judge_key_not_null(params, "store_state"):
            model = model.filter(AssetConsumeInfoModel.store_state_id == params['store_state'])
        if judge_key_not_null(params, "device_state"):
            model = model.filter(AssetConsumeInfoModel.device_state_id == params['device_state'])
        if judge_key_not_null(params, "store_place"):
            model = model.filter(AssetConsumeInfoModel.store_place_id == params['store_place'])
        if judge_key_not_null(params, "in_out_reason"):
            model = model.filter(AssetConsumeInfoModel.in_out_reason_id == params['in_out_reason'])
        if judge_key_not_null(params, "asset_type"):
            model = model.filter(AssetConsumeInfoModel.asset_type_id == params['asset_type'])
        if judge_key_not_null(params, "date_from1"):
            model = model.filter(AssetConsumeInfoModel.up_time >= params['date_from1'])
        if judge_key_not_null(params, "date_to1"):
            model = model.filter(AssetConsumeInfoModel.up_time <= params['date_to1'])
        if judge_key_not_null(params, "date_from2"):
            model = model.filter(AssetConsumeInfoModel.update_time >= params['date_from2'])
        if judge_key_not_null(params, "date_to2"):
            model = model.filter(AssetConsumeInfoModel.update_time <= params['date_to2'])
        # if params['oper_name'] != "":
        #     model = model.filter(AssetConsumeInfoModel.asset_id.in_(params["asset_id_list"]))
        return model

    def get_advanced_search_val_all_datas(self, params):
        return self.get_advanced_consume_search_val(params).all()

    def get_asset_info_excel_by_search_val_all(self, id):
        model = self.get_consume_asset_info_sql(id)
        return model.all()