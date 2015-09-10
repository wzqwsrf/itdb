# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


import json
from itdblib.dal.model_dal import ModelDal
from itdblib.dal.provider_dal import ProviderDal
from itdblib.dal.asset_type_dal import AssetTypeDal
from itdblib.dal.device_state_dal import DeviceStateDal
from itdblib.dal.store_state_dal import StoreStateDal
from itdblib.dal.store_place_dal import StorePlaceDal
from itdblib.dal.in_out_reason_dal import InOutReasonDal
from qg.core import log as logging
import sys
LOG = logging.getLogger(__name__)
reload(sys)
sys.setdefaultencoding('utf8')


class ConstructDictService():

    def __init__(self):
        LOG.info('init StockInService!')

    # 获取型号数字和中文对应值'''
    def get_model_dict(self):
        models = ModelDal().get_model_all()
        model_dicts = dict([(at.id, at.name) for at in models])
        return model_dicts

    # 获取型号中文和数字对应值'''
    def get_model_ch_dict(self):
        models = ModelDal().get_model_all()
        model_ch_dicts = dict([(at.name, at.id) for at in models])
        return model_ch_dicts

    def get_prov_model_dict(self):
        models = ModelDal().get_model_all()
        prov_model_dicts = dict([(at.provider_id, at.id) for at in models])
        return prov_model_dicts

    # 获取型号和品牌对应值
    def get_model_prov_dict(self):
        models = ModelDal().get_model_all()
        model_prov_dicts = dict([(at.id, at.provider_id) for at in models])
        return model_prov_dicts

    # 获取品牌数字和中文对应值
    def get_provider_dict(self):
        providers = ProviderDal().get_provider_all()
        prov_dicts = dict([(at.id, at.name) for at in providers])
        return prov_dicts

    # 根据asset_type_id和品牌获取id
    def get_provtype_dict(self):
        providers = ProviderDal().get_provider_all()
        prov_type_dicts = dict([('_'.join([str(at.asset_type_id),
                            at.name]), at.id) for at in providers])
        return prov_type_dicts

    def get_provmodel_dict(self):
        models = ModelDal().get_model_all()
        prov_model_dicts = dict([('_'.join([str(at.provider_id),
                            at.name]), at.id) for at in models])
        return prov_model_dicts

    # 获取资产类别数字和中文对应值
    def get_asset_type_dict(self):
        asset_types = AssetTypeDal().get_asset_type_all()
        return self.trans_list_to_dict_en(asset_types)

    # 获取设备状态数字和中文对应值
    def get_device_state_dict(self):
        device_states = DeviceStateDal().get_all_device_state()
        return self.trans_list_to_dict_en(device_states)

    # 获取资产类别中文和数字对应值
    def get_asset_type_ch_dict(self):
        asset_types = AssetTypeDal().get_asset_type_all()
        return self.trans_list_to_dict_ch(asset_types)

    # 获取设备状态中文和数字对应值
    def get_device_state_ch_dict(self):
        device_states = DeviceStateDal().get_all_device_state()
        return self.trans_list_to_dict_ch(device_states)

    # 获取所有的设备类别list
    def get_asset_type_list(self):
        asset_types = AssetTypeDal().get_asset_type_all()
        return self.get_all_dict_list(asset_types)

    # 获取所有的设备状态list
    def get_device_state_list(self):
        device_states = DeviceStateDal().get_all_device_state()
        return self.get_all_dict_list(device_states)

    # 获取库存状态数字和中文对应值
    def get_store_state_dict(self):
        store_states = StoreStateDal().get_store_state_all()
        return self.trans_list_to_dict_en(store_states)

    # 获取库存状态中文和数字对应值
    def get_store_state_ch_dict(self):
        store_states = StoreStateDal().get_store_state_all()
        return self.trans_list_to_dict_ch(store_states)

    # 获取存放地点数字和中文对应值
    def get_store_place_dict(self):
        store_places = StorePlaceDal().get_store_place_all()
        return self.trans_list_to_dict_en(store_places)

    # 获取存放地点中文和数字对应值
    def get_store_place_ch_dict(self):
        store_places = StorePlaceDal().get_store_place_all()
        return self.trans_list_to_dict_ch(store_places)

    # 获取出入库原因数字和中文对应值
    def get_in_out_dict(self):
        in_out_reasons = InOutReasonDal().get_in_out_reason_all()
        return self.trans_list_to_dict_en(in_out_reasons)

    # 获取出入库原因中文和数字对应值
    def get_in_out_ch_dict(self):
        in_out_reasons = InOutReasonDal().get_in_out_reason_all()
        return self.trans_list_to_dict_ch(in_out_reasons)

    # 获取库存状态list
    def get_store_state_list(self):
        store_states = StoreStateDal().get_store_state_all()
        return self.get_all_dict_list(store_states)

    # 获取库存地点list
    def get_store_place_list(self):
        store_places = StorePlaceDal().get_store_place_all()
        return self.get_all_dict_list(store_places)

    # 获取入库原因list
    def get_in_reason_list(self):
        in_reasons = InOutReasonDal().get_in_reason_all()
        return self.get_all_dict_list(in_reasons)

    # 获取出库原因list
    def get_out_reason_list(self):
        out_reasons = InOutReasonDal().get_out_reason_all()
        return self.get_all_dict_list(out_reasons)

    # 封装内部调用
    def get_all_dict_list(self, infos):
        ret = []
        for info in infos:
            params = {}
            params["id"] = info.id
            params["ch_name"] = info.ch_name
            ret.append(params)
        return json.dumps(ret)

    def trans_list_to_dict_ch(self, infos):
        return dict([(info.ch_name, info.id) for info in infos])

    def trans_list_to_dict_en(self, infos):
        return dict([(info.id, info.ch_name) for info in infos])

    def construct_type_info(self, new_data):
        from itdblib.common.type_info_utils import type_info_en_list
        type_infos = type_info_en_list()
        d_len = len(type_infos)
        type_info = {}
        for i in range(d_len):
            key = type_infos[i]
            value = new_data.get(key)
            if value:
                value = str(new_data[key]).upper()
                type_info[key] = value
        return type_info