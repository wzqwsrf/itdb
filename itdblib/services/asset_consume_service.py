# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import json
from qg.core import log as logging
from itdblib.services.asset_info_ch_name_to_id import AssetInfoChNameToId
from itdblib.services.asset_info_id_to_ch_name import AssetInfoIdToChName
from itdblib.services.asset_info_service import AssetInfoService
from itdblib.services.asset_operate_service import AssetOperateService
from itdblib.dal.asset_consume_info_dal import AssetConsumeInfoDal
from itdblib.common.corehr_api_utils import get_actual_rtx_id
from itdblib.common.time_utils import trans_time
from itdblib.common.asset_info_utils import AssetInfoUtils
LOG = logging.getLogger(__name__)


class AssetConsumeService():
    def __init__(self):
        LOG.info('init AssetConsumeService!')

    def get_asset_consume_info_all_show(self, start, count):
        aci = AssetConsumeInfoDal()
        assetInfos = aci.get_asset_consume_info_limit(start, count)
        count = aci.get_asset_consume_info_num()
        return self.get_asset_consume_info_all(assetInfos, count)

    def get_asset_consume_info_all(self, assetInfos, count):
        ret = []
        for assetInfo in assetInfos:
            params = self.get_asset_consume_table_info(assetInfo)
            ret.append(params)
        rets = {'data': ret, 'count': count}
        return json.dumps(rets)

    def get_asset_consume_info_search_show(self, id, start, count):
        rtx_id = get_actual_rtx_id(id)
        assetInfos = AssetConsumeInfoDal(). \
            get_asset_consume_info_by_search_val_all(rtx_id, start, count)
        count = self.get_asset_consume_infos_num_by_search_val(rtx_id)
        return self.get_asset_consume_info_all(assetInfos, count)

    def get_asset_consume_infos_num_by_search_val(self, id):
        rtx_id = get_actual_rtx_id(id)
        return AssetConsumeInfoDal().get_asset_consume_info_query_num(rtx_id)

    def get_prov_model_place_num(self, params):
        aio = AssetInfoChNameToId()
        list = aio.get_asset_type_and_model_id(params)
        asset_type_id = list[0]
        model_id = list[1]
        store_place_id = aio. \
            get_store_place_id_by_ch_name(params['store_place'])
        assetInfo = AssetConsumeInfoDal().get_asset_type_model_place_num(
            asset_type_id, model_id, store_place_id)
        ret_params = {}
        if assetInfo:
            ret_params['in_num1'] = str(assetInfo.in_num)
            ret_params['user_name'] = assetInfo.user_name
        return json.dumps(ret_params)

    def get_prov_model_user_name_num(self, params):
        aio = AssetInfoChNameToId()
        list = aio.get_asset_type_and_model_id(params)
        asset_type_id = list[0]
        model_id = list[1]
        print list
        assetInfo = AssetConsumeInfoDal().get_asset_type_model_user_name_num(
            asset_type_id, model_id, params["user_name"], 2)
        print assetInfo
        ret_params = {}
        if assetInfo:
            ret_params['in_num'] = str(assetInfo.in_num)
            ret_params['user_name'] = assetInfo.user_name
        return json.dumps(ret_params)

    def store_out_add_consume_data(self, data, operator):
        new_data = {}
        for k, v in data.items():
            new_data[k] = v
        # self.construct_out_oper_data(new_data, operator)
        aio = AssetInfoChNameToId()
        list = aio.get_asset_type_and_model_id(new_data)
        new_data["asset_type"] = list[0]
        new_data["model"] = list[1]
        new_data["store_place1"] = aio. \
            get_store_place_id_by_ch_name(new_data['store_place1'])
        new_data["store_place2"] = aio. \
            get_store_place_id_by_ch_name(new_data['store_place2'])
        new_data["store_state"] = aio. \
            get_store_state_id_by_ch_name('在用')
        new_data["device_state"] = aio. \
            get_store_state_id_by_ch_name('可用')
        new_data['in_out_reason'] = aio.\
            get_in_out_reason_id_by_ch_name(data['in_out_reason'])
        return AssetConsumeInfoDal().store_old_consume_data(new_data)

    def get_asset_consume_info_id_ch_name(self, assetConsumeInfo):
        params = self.get_asset_consume_table_info(assetConsumeInfo)
        aic = AssetInfoIdToChName()
        params['model'] = aic.get_model_name_by_num(assetConsumeInfo.model_id)
        params['provider'] = aic.get_prov_name_by_num(assetConsumeInfo.asset_type_id,
                                                      assetConsumeInfo.model_id)
        params['in_out_reason'] = aic.get_in_out_reason_name_by_num(
                                        assetConsumeInfo.in_out_reason_id)
        params['user_name'] = assetConsumeInfo.user_name
        params['remark'] = assetConsumeInfo.remark
        params['create_time'] = trans_time(assetConsumeInfo.create_time)
        params['update_time'] = trans_time(assetConsumeInfo.update_time)
        params['up_time'] = trans_time(assetConsumeInfo.up_time)
        params['out_num'] = assetConsumeInfo.out_num
        params['consume_all'] = int(assetConsumeInfo.in_num) + int(assetConsumeInfo.out_num)
        return params

    def get_asset_consume_table_info(self, assetConsumeInfo):
        params = {}
        if assetConsumeInfo is None:
            return params
        params['id'] = assetConsumeInfo.id
        aic = AssetInfoIdToChName()
        params['asset_type'] = aic.get_asset_type_name_by_num(assetConsumeInfo.asset_type_id)
        params['store_state'] = aic.get_store_state_name_by_num(
                                    assetConsumeInfo.store_state_id)
        params['store_place'] = aic.get_store_place_name_by_num(
                                    assetConsumeInfo.store_place_id)
        params['user_name'] = assetConsumeInfo.user_name
        params['in_num'] = assetConsumeInfo.in_num
        params['device_state'] = aic.get_device_state_name_by_num(assetConsumeInfo.device_state_id)
        return params

    def store_new_consume_info(self, data):
        acd = AssetInfoChNameToId()
        data = acd.trans_ch_data_to_id(data)
        data["in_num"] = int(data["in_num1"]) + int(data["in_num2"])
        return AssetConsumeInfoDal().store_new_consume_data(data)


    def get_asset_consume_info_by_id(self, consume_id):
        assetInfo = AssetConsumeInfoDal().get_consume_asset_info_by_id(consume_id)
        if assetInfo is None:
            return ''
        ret = []
        params = self.get_asset_consume_info_id_ch_name(assetInfo)
        ret.append(params)
        return json.dumps(ret)

    def get_asset_consume_info_by_rtx_id(self, consume_id):
        assetInfo = AssetConsumeInfoDal().get_asset_consume_info_by_search_val_one(consume_id)
        if assetInfo is None:
            return ''
        ret = []
        params = self.get_asset_consume_info_id_ch_name(assetInfo)
        ret.append(params)
        return json.dumps(ret)

    def store_consume_old_add_data(self, data):
        new_data = {}
        for k, v in data.items():
            new_data[k] = v
        self.store_consume_old_data(new_data)
        ret, msg = AssetConsumeInfoDal().store_old_consume_in_data(new_data)
        return ret, msg

    def store_consume_old_data(self, data):
        aci = AssetInfoChNameToId()
        data['old_user_name'] = data['user_name_c']
        data['user_name'] = data['c_user_name']
        data['store_state'] = aci.\
                get_store_state_id_by_ch_name(data['c_store_state'])
        data['store_place'] = aci.\
                get_store_place_id_by_ch_name(data['c_store_place'])
        data['in_out_reason'] = aci.\
                get_in_out_reason_id_by_ch_name(data['c_in_out_reason'])
        data['device_state'] = aci.\
                get_device_state_id_by_ch_name(data['c_device_state'])
        data['remark'] = data['c_remark']
        list = aci.get_asset_type_and_model_id(data)
        data["asset_type"] = list[0]
        data["model"] = list[1]

    def get_asset_consume_info_advanced_search_show(self, request_params, start, count):
        ais = AssetInfoService()
        params = ais.get_advanced_web_params(request_params)
        return self.get_advanced_consume_search_val_all(params, start, count)

    def get_advanced_consume_search_val_all(self, params, start, count):
        aid = AssetConsumeInfoDal()
        assetInfos = aid.get_advanced_consume_search_val_limit(params, start, count)
        count = aid.get_advanced_consume_search_val_count(params)
        return self.get_asset_consume_info_all(assetInfos, count)

    def get_export_excel_data(self, key):
        if key != "":
            # 传递过来的值包含=，是高级查询
            if key.find("=") >= 0:
                ais = AssetInfoService()
                params = ais.get_data_by_split_web(key)
                params = ais.get_advanced_web_params(params)
                assetInfos = AssetConsumeInfoDal().get_advanced_search_val_all_datas(params)
            # 一般查询
            else:
                rtx_id = get_actual_rtx_id(key)
                assetInfos = AssetConsumeInfoDal().get_asset_info_excel_by_search_val_all(rtx_id)
        else:
            assetInfos = AssetConsumeInfoDal().get_asset_consume_info_all()

        ret = []
        for assetInfo in assetInfos:
            params = self.get_asset_consume_info_id_ch_name(assetInfo)
            ret.append(params)
        return ret

    def get_consume_operate_json(self, operInfos):
        aos = AssetOperateService()
        en_ch_dict = self.get_consume_en_ch_dict()
        return aos.get_operate_json(operInfos, en_ch_dict)

    def get_consume_en_ch_dict(self):
        aiu = AssetInfoUtils()
        enlist = aiu.get_consume_en_list()
        chlist = aiu.get_consume_ch_list()
        d_len = len(enlist)
        return dict([(enlist[i], chlist[i]) for i in range(d_len)])

    def construct_out_oper_data(self, new_data, operator):
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