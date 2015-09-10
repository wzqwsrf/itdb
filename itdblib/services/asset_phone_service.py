# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import json
from qg.core import log as logging
from itdblib.services.asset_info_ch_name_to_id import AssetInfoChNameToId
from itdblib.services.asset_info_id_to_ch_name import AssetInfoIdToChName
from itdblib.services.asset_operate_service import AssetOperateService
from itdblib.services.asset_info_service import AssetInfoService
from itdblib.dal.asset_phone_info_dal import AssetPhoneInfoDal
from itdblib.dal.operation_info_dal import OperationInfoDal
from itdblib.common.time_utils import trans_time
from itdblib.common.corehr_api_utils import get_actual_rtx_id
from itdblib.common.corehr_api_utils import get_employee_owner
from itdblib.common.asset_info_utils import AssetInfoUtils


LOG = logging.getLogger(__name__)


class AssetPhoneService():
    def __init__(self):
        LOG.info('init AssetPhoneService!')

    def get_asset_phone_info_all_show(self, start, count):
        aci = AssetPhoneInfoDal()
        assetInfos = aci.get_asset_phone_info_limit(start, count)
        count = aci.get_asset_phone_info_num()
        return self.get_asset_phone_info_all(assetInfos, count)

    def get_asset_phone_info_all(self, assetInfos, count):
        ret = []
        for assetInfo in assetInfos:
            params = self.get_asset_phone_show_info(assetInfo)
            ret.append(params)
        rets = {'data': ret, 'count': count}
        return json.dumps(rets)

    def get_asset_phone_info_search_show(self, id, start, count):
        rtx_id = get_actual_rtx_id(id)
        assetInfos = AssetPhoneInfoDal(). \
            get_asset_phone_info_by_search_val_all(rtx_id, start, count)
        count = self.get_asset_phone_infos_num_by_search_val(rtx_id)
        return self.get_asset_phone_info_all(assetInfos, count)

    def get_asset_phone_infos_num_by_search_val(self, id):
        rtx_id = get_actual_rtx_id(id)
        return AssetPhoneInfoDal().get_asset_phone_info_query_num(rtx_id)

    def get_prov_model_place_num(self, params):
        aio = AssetInfoChNameToId()
        list = aio.get_asset_type_and_model_id(params)
        asset_type_id = list[0]
        model_id = list[1]
        store_place_id = aio. \
            get_store_place_id_by_ch_name(params['store_place'])
        return AssetPhoneInfoDal().get_asset_type_model_place_num(
            asset_type_id, model_id, store_place_id)

    def store_new_add_phone_data(self, params):
        data = {}
        aio = AssetInfoChNameToId()
        list = aio.get_asset_type_and_model_id(params)
        data["asset_type_id"] = list[0]
        data["model_id"] = list[1]
        data["user_name"] = params["user_name"]
        data["phone_num"] = int(params["phone_num1"]) + int(params["phone_num2"])
        data["phone_num1"] = params["phone_num1"]
        data["phone_num2"] = params["phone_num2"]
        data["store_place_id"] = aio. \
            get_store_place_id_by_ch_name(params['store_place'])
        data["remark"] = params["remark"]
        return AssetPhoneInfoDal().store_new_phone_data(data)

    def get_asset_phone_info_id_ch_name(self, assetPhoneInfo):
        params = {}
        if assetPhoneInfo is None:
            return params
        aic = AssetInfoIdToChName()
        params = self.get_asset_phone_show_info(assetPhoneInfo)
        params['in_out_reason'] = aic.get_in_out_reason_name_by_num(
                                        assetPhoneInfo.in_out_reason_id)
        params['remark'] = assetPhoneInfo.remark
        params['up_time'] = trans_time(assetPhoneInfo.up_time)
        params['create_time'] = trans_time(assetPhoneInfo.create_time)
        params['update_time'] = trans_time(assetPhoneInfo.update_time)
        return params

    def get_asset_phone_info_by_id(self, phone_no):
        assetInfo = AssetPhoneInfoDal().get_asset_phone_info_by_search_val_one(phone_no)
        if assetInfo is None:
            return ''
        ret = []
        params = self.get_phone_detail_asset_info(assetInfo)
        ret.append(params)
        return json.dumps(ret)

    def get_phone_detail_asset_info(self, assetInfo):
        params = self.get_asset_phone_info_id_ch_name(assetInfo)
        params['owner'] = get_employee_owner(assetInfo.user_name)
        operInfo = OperationInfoDal().get_oper_info_by_asset_id(assetInfo.phone_no)
        params['operator'] = '' if not operInfo\
                            else operInfo['operator']
        return params

    def get_asset_phone_show_info(self, assetInfo):
        params = {}
        if assetInfo is None:
            return params
        aic = AssetInfoIdToChName()
        params['asset_type'] = aic.get_asset_type_name_by_num(assetInfo.asset_type_id)
        params['phone_no'] = assetInfo.phone_no
        params['store_state'] = aic.get_store_state_name_by_num(
                                        assetInfo.store_state_id)
        params['device_state'] = aic.get_device_state_name_by_num(
                                        assetInfo.device_state_id)
        params['user_name'] = assetInfo.user_name
        params['store_place'] = aic.get_store_place_name_by_num(
                                        assetInfo.store_place_id)
        return params

    def get_phone_operate_json(self, operInfos):
        aos = AssetOperateService()
        en_ch_dict = self.get_phone_en_ch_dict()
        return aos.get_operate_json(operInfos, en_ch_dict)

    def get_phone_en_ch_dict(self):
        aiu = AssetInfoUtils()
        enlist = aiu.get_phone_en_list()
        chlist = aiu.get_phone_ch_list()
        d_len = len(enlist)
        return dict([(enlist[i], chlist[i]) for i in range(d_len)])

    def get_asset_phone_info_advanced_search_show(self, request_params, start, count):
        ais = AssetInfoService()
        params = ais.get_advanced_web_params(request_params)
        return self.get_advanced_phone_search_val_all(params, start, count)

    def get_advanced_phone_search_val_all(self, params, start, count):
        aid = AssetPhoneInfoDal()
        assetInfos = aid.get_advanced_phone_search_val_limit(params, start, count)
        count = aid.get_advanced_phone_search_val_count(params)
        return self.get_asset_phone_info_all(assetInfos, count)

    def store_phone_old_add_data(self, data):
        new_data = {}
        for k, v in data.items():
            new_data[k] = v
        new_data = self.store_phone_old_data(new_data)
        ret, msg = AssetPhoneInfoDal().update_asset_phone_info_by_id(new_data)
        return ret, msg

    def store_phone_old_data(self, data):
        aci = AssetInfoChNameToId()
        new_data = {}
        new_data['phone_no'] = data['phone_no']
        new_data['user_name'] = data['p_user_name']
        new_data['store_state'] = aci.\
                get_store_state_id_by_ch_name(data['p_store_state'])
        new_data['store_place'] = aci.\
                get_store_place_id_by_ch_name(data['p_store_place'])
        new_data['in_out_reason'] = aci.\
                get_in_out_reason_id_by_ch_name(data['p_in_out_reason'])
        new_data['device_state'] = aci.\
                get_device_state_id_by_ch_name(data['p_device_state'])
        new_data['remark'] = data['p_remark']
        return new_data

    def get_phone_out_data(self, data):
        new_data = {}
        for k, v in data.items():
            new_data[k] = v
        new_data = self.get_actual_num_data(new_data)
        ret, msg = AssetPhoneInfoDal().get_phone_out_data(new_data)
        if ret:
            params = []
            count = len(ret)
            for i in range(count):
                params.append(ret[i].phone_no)
            rets = {'data': params, 'count': count}
        else:
            rets = {'data': [], 'count': 0}
        return json.dumps(rets)

    def get_actual_num_data(self, data):
        aci = AssetInfoChNameToId()
        data['store_state'] = aci.\
                get_store_state_id_by_ch_name('库存')
        data['store_place'] = aci.\
                get_store_place_id_by_ch_name(data['store_place'])
        data['device_state'] = aci.\
                get_device_state_id_by_ch_name('可用')
        data['asset_type'] = aci.get_id_by_at_asset_ch_name(data['asset_type'])
        return data

    def get_actual_out_num_data(self, data):
        aci = AssetInfoChNameToId()
        data['store_place'] = aci.\
                get_store_place_id_by_ch_name(data['store_place'])
        data['in_out_reason'] = aci.\
                get_in_out_reason_id_by_ch_name(data['in_out_reason'])
        data['store_state'] = aci.\
                get_store_state_id_by_ch_name('在用')
        return data

    def store_phone_out_data(self, data, operator):
        new_data = {}
        for k, v in data.items():
            new_data[k] = v
        self.construct_out_oper_data(new_data, operator)
        new_data = self.get_actual_out_num_data(new_data)
        return AssetPhoneInfoDal().update_asset_phone_info_out(new_data)

    def construct_out_oper_data(self, new_data, operator):
        assetInfo = AssetPhoneInfoDal().get_asset_phone_info_by_search_val_one(new_data['phone_no'])
        aic = AssetInfoIdToChName()
        params_o = {}
        params_o['in_out_reason'] = aic.get_in_out_reason_name_by_num(
                                        assetInfo.in_out_reason_id)
        params_o['store_state'] = aic.get_store_state_name_by_num(
                                        assetInfo.store_state_id)
        params_o['device_state'] = aic.get_device_state_name_by_num(
                                        assetInfo.device_state_id)
        params_o['user_name'] = assetInfo.user_name
        params_o['store_place'] = aic.get_store_place_name_by_num(
                                        assetInfo.store_place_id)
        params_o['phone_no'] = assetInfo.phone_no
        params_o['asset_type'] = aic.get_asset_type_name_by_num(assetInfo.asset_type_id)
        params_o['remark'] = assetInfo.remark
        params_n = {}
        params_n['store_place'] = new_data['store_place']
        params_n['in_out_reason'] = new_data['in_out_reason']
        params_n['store_state'] = '在用'
        params_n['remark'] = new_data['remark']

        oper_data = {}
        oper_data['asset_id'] = params_o['phone_no']
        oper_data['oper_type'] = '字段变更'
        oper_data['operator'] = operator
        oper_data['text'] = ''
        aiu = AssetInfoUtils()
        enlist = aiu.get_oper_phone_enlist()
        e_len = len(enlist)
        before_field = ''
        after_field = ''
        for i in range(e_len):
            before_field += enlist[i] + ":" + params_o[enlist[i]] + ","
            if params_n.has_key(enlist[i]):
                after_field += enlist[i] + ":" + params_n[enlist[i]] + ","
            else:
                after_field += enlist[i] + ":" + params_o[enlist[i]] + ","
        oper_data['before_field'] = before_field
        oper_data['after_field'] = after_field
        ais = AssetInfoService()
        ais.save_oper_info(oper_data)

    def get_export_excel_data(self, key):
        if key != "":
            # 传递过来的值包含=，是高级查询
            if key.find("=") >= 0:
                ais = AssetInfoService()
                params = ais.get_data_by_split_web(key)
                params = ais.get_advanced_web_params(params)
                assetInfos = AssetPhoneInfoDal().get_advanced_search_val_all_datas(params)
            # 一般查询
            else:
                rtx_id = get_actual_rtx_id(key)
                assetInfos = AssetPhoneInfoDal().get_asset_info_excel_by_search_val_all(rtx_id)
        else:
            assetInfos = AssetPhoneInfoDal().get_asset_phone_info_all()

        ret = []
        for assetInfo in assetInfos:
            params = self.get_asset_phone_info_id_ch_name(assetInfo)
            ret.append(params)
        return ret