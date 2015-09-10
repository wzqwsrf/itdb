# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from qg.core import log as logging
from itdblib.common.corehr_api_utils import get_actual_rtx_id
from itdblib.common.asset_info_utils import AssetInfoUtils
from itdblib.services.asset_info_id_to_ch_name import AssetInfoIdToChName
from itdblib.services.asset_info_ch_name_to_id import AssetInfoChNameToId
from itdblib.dal.operation_info_dal import OperationInfoDal
from itdblib.dal.provider_dal import ProviderDal
from itdblib.dal.model_dal import ModelDal
from itdblib.dal.asset_phone_info_dal import AssetPhoneInfoDal
from itdblib.dal.asset_info_dal import AssetInfoDal
from itdblib.dal.store_place_dal import StorePlaceDal
import json
LOG = logging.getLogger(__name__)


class AssetInfoService():
    def get_asset_info_show(self, search_val):
        rtx_id = get_actual_rtx_id(search_val)
        return self.get_asset_info_by_id(rtx_id)

    def validate_add_new_asset_info(self, data):
        validate_ret, msg = self.validate_web_data(data, 1)
        if validate_ret is False:
            return False, msg
        validate_ret, msg = self.validate_value_is_single(data)
        if validate_ret is False:
            return False, msg
        aci = AssetInfoChNameToId()
        new_data = aci.trans_ch_data_to_id(data)
        validate_ret, msg = self.validate_web_data(new_data, 2)
        if validate_ret is False:
            return False, msg
        return True, new_data

    def validate_web_data(self, data, num):
        enlist = AssetInfoUtils().add_asset_info_en_list()
        d_len = len(enlist)
        for i in range(d_len):
            if num != 1 and enlist[i] == 'provider':
                continue
            if enlist[i] in data and (data[enlist[i]] is None or data[enlist[i]] == ''):
                error_msg = 'asset_id为' + data['asset_id'] + '的' + enlist[i] + ' value is None！'
                LOG.error(error_msg)
                return False, error_msg
        return True, 'validate_web_data success'

    def validate_value_is_single(self, data):
        keys = ['asset_id', 'mac', 'sn', 'imei']
        k_len = len(keys)
        for i in range(k_len):
            ret, msg = self.actual_judge_value_is_single(data, keys[i])
            if not ret:
                return ret, msg
        return True, 'validate_value_is_single success'

    def actual_judge_value_is_single(self, data, key):
        if key in data and data[key] is not None and data[key] != '':
            asset_info = None
            if key == 'asset_id':
                asset_info = AssetInfoDal().get_asset_info_by_id(data['asset_id'])
            elif key == 'sn':
                asset_info = AssetInfoDal().get_asset_info_by_sn(data['sn'])
            elif key == 'mac':
                asset_info = AssetInfoDal().get_asset_info_by_mac(data['mac'])
            elif key == 'imei':
                asset_info = AssetInfoDal().get_asset_info_by_imei(data['imei'])
            if asset_info is not None:
                error_msg = u'数据库表TB_ASSET_INFO已经有 ' + key + ' = ' + data[key] + ', 请检查！'
                LOG.error(error_msg)
                return False, error_msg
            if key != 'asset_id':
                asset_info = AssetInfoDal().get_asset_info_by_all_unique(data[key])
                if asset_info is not None:
                    error_msg = u'数据库表TB_ASSET_INFO已经有sn/mac/imei ' + ' = ' + data[key] + ', 请检查！'
                    LOG.error(error_msg)
                    return False, error_msg
        return True, key + 'validate_value_is_single success'

    def validate_phone_is_single(self, data):
        key = 'phone_no'
        if key in data and data[key] is not None and data[key] != '':
            assetInfo = AssetPhoneInfoDal().get_phone_asset_info_by_phone_no(data[key])
            if assetInfo is not None:
                error_msg = u'数据库表TB_ASSET_PHONE_INFO已经有电话号码 ' + ' = ' + data[key] + ', 请检查！'
                LOG.error(error_msg)
                return False, error_msg
        return True, data[key] + ' validate_phone_is_single success'

    def store_old_add_data(self, data):
        aci = AssetInfoChNameToId()
        new_data = {}
        for k, v in data.items():
            new_data[k] = v
        new_data['asset_ids'] = data['asset_id']
        new_data = aci.store_in_out_old_data(new_data)
        ret, msg = AssetInfoDal().update_asset_info_by_id(new_data)
        return ret, msg

    def get_asset_info_by_id(self, asset_id):
        assetInfo = AssetInfoDal().get_asset_info_by_search_val_one(asset_id)
        if assetInfo is None:
            return ''
        aic = AssetInfoIdToChName()
        ret = []
        params = aic.get_detail_asset_info(assetInfo)
        ret.append(params)
        return json.dumps(ret)

    def save_oper_info(self, data):
        before_field = self.transform_hstore_val(
            data['before_field'].split(','))
        after_field = self.transform_hstore_val(
            data['after_field'].split(','))
        from itdblib.dal.operation_info_dal import OperationInfoDal

        OperationInfoDal().add_oper_infos(str(data['asset_id']).upper(), data['oper_type'],
                                          data['operator'], data['text'],
                                          before_field, after_field)

    def transform_hstore_val(self, field_msg):
        hstore_val = {}
        # 这里为了删掉逗号，所以是len-1
        for i in range(len(field_msg) - 1):
            detail = field_msg[i].split(':')
            hstore_val[detail[0]] = "" if detail[1] is None else detail[1]
        return hstore_val

    def get_owner_by_rtx_id(self, rtx_id):
        from itdblib.common.corehr_api_utils import get_employee_owner
        return get_employee_owner(rtx_id)

    def get_prov_list_by_type(self, asset_type):
        aoc = AssetInfoChNameToId()
        id = aoc.get_id_by_at_asset_ch_name(asset_type)
        return ProviderDal().get_prov_by_asset_type(id)

    def get_model_by_prov(self, asset_type, provider):
        # 根据品牌得到所有的该品牌的型号
        aoc = AssetInfoChNameToId()
        id = aoc.get_id_by_at_asset_ch_name(asset_type)
        prov_model = ProviderDal().get_prov_by_id_and_at(id, provider)
        modelList = ModelDal().get_model_by_prov_id(prov_model.id)
        models = []
        for model in modelList:
            models.append(model.name)
        return models

    def get_employee_by_input(self, rtx_id):
        from itdblib.common.hr_intf import auto_show_employee_info

        return auto_show_employee_info(rtx_id)

    def get_advanced_web_params(self, request_params):
        list = AssetInfoUtils().get_advanced_list()
        d_len = len(list)
        params = {}
        for i in range(d_len):
            params[list[i]] = request_params[list[i]]
        ait = AssetInfoChNameToId()
        if params['store_state'] != "":
            params["store_state"] = ait. \
                get_store_state_id_by_ch_name(params['store_state'])
        if params['device_state'] != "":
            params["device_state"] = ait. \
                get_device_state_id_by_ch_name(params['device_state'])
        if params['store_place'] != "":
            params["store_place"] = ait. \
                get_store_place_id_by_ch_name(params['store_place'])
        params["in_out_reason"] = ""
        if params['in_reason'] != "":
            params["in_out_reason"] = ait. \
                get_in_out_reason_id_by_ch_name(params['in_reason'])
        if params['out_reason'] != "":
            params["in_out_reason"] = ait. \
                get_in_out_reason_id_by_ch_name(params['out_reason'])
        if params['asset_type'] != "":
            params["asset_type"] = ait. \
                get_id_by_at_asset_ch_name(params['asset_type'])
        if params['provider'] != "":
            params["provider"] = ait. \
                get_prov_id_by_atd_ch(params["asset_type"], params['provider'])
        if params['model'] != "" and \
                        params['provider'] != "":
            params["model"] = ait. \
                get_model_id_by_pd_ch(params["provider"], params['model'])
        params["model_list"] = []
        if params['provider'] != "":
            if params["model"] == "":
                params["model_list"] = ModelDal().get_model_list_by_prov_id(params['provider'])
        if params["oper_name"] != "":
            params["asset_id_list"] = OperationInfoDal().get_asset_id_list_by_operator(params["oper_name"])
        return params

    def get_asset_info_three_info_by_id(self, asset_id):
        asset_infos = AssetInfoDal().get_asset_info_first_by_id(asset_id)
        aic = AssetInfoIdToChName()
        params = []
        for asset_info in asset_infos:
            msg = asset_info.asset_id + '(' + \
                  aic.get_asset_type_name_by_num(asset_info.asset_type_id) \
                  + '-' + aic.get_store_place_name_by_num(asset_info.store_place_id)\
                  + '-' + asset_info.user_name\
                  + ')'
            params.append(msg)
        return params

    def get_data_by_split_web(self, key):
        params = {}
        keyList = key.split(",")
        k_len = len(keyList)
        for i in range(k_len):
            inkey = keyList[i].split("=")
            if len(inkey) == 1:
                params[inkey[0]] = ""
            else:
                params[inkey[0]] = inkey[1]
        return params

    def get_admin_name_by_store_place(self, store_place):
        admins = []
        storeModel = StorePlaceDal().get_admin_name_by_ch_name(store_place)
        if storeModel:
            admins.append(storeModel.admin_name)
        return json.dumps(admins)