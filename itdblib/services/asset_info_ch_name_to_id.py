# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from itdblib.dal.asset_type_dal import AssetTypeDal
from itdblib.dal.model_dal import ModelDal
from itdblib.dal.device_state_dal import DeviceStateDal
from itdblib.dal.store_state_dal import StoreStateDal
from itdblib.dal.store_place_dal import StorePlaceDal
from itdblib.dal.in_out_reason_dal import InOutReasonDal
from itdblib.dal.provider_dal import ProviderDal
from itdblib.common.asset_info_utils import AssetInfoUtils


class AssetInfoChNameToId():

    def get_asset_info_common_data(self, data):
        asset_type_id = self.get_id_by_at_asset_ch_name(data['asset_type'])
        data['asset_type'] = asset_type_id
        data['device_state'] = self.\
                get_device_state_id_by_ch_name(data['device_state'])
        data['store_state'] = self.\
                get_store_state_id_by_ch_name(data['store_state'])
        data['store_place'] = self.\
                get_store_place_id_by_ch_name(data['store_place'])
        data['in_out_reason'] = self.\
                get_in_out_reason_id_by_ch_name(data['in_out_reason'])
        return data

    def trans_ch_data_to_id(self, data):
        data = self.get_asset_info_common_data(data)
        data['model'] = self.get_model_id_by_asset_type_pd(
                            data['asset_type'],
                            data['provider'],
                            data['model'])
        return data

    def store_in_out_old_data(self, data):
        new_data = {}
        new_data['asset_id'] = data['asset_ids']
        new_data['user_name'] = data['user_names']
        new_data['store_state'] = self.\
                get_store_state_id_by_ch_name(data['store_states'])
        new_data['store_place'] = self.\
                get_store_place_id_by_ch_name(data['store_places'])
        new_data['in_out_reason'] = self.\
                get_in_out_reason_id_by_ch_name(data['in_out_reasons'])
        new_data['device_state'] = self.\
                get_device_state_id_by_ch_name(data['device_states'])
        new_data['remark'] = data['remarks']
        return new_data

    def get_id_by_at_asset_ch_name(self, asset_type):
        atd = AssetTypeDal()
        assetType = atd.get_asset_type_id_by_ch_name(asset_type)
        return self.actual_return_id_val(assetType)

    def get_prov_id_by_atd_ch(self, asset_type_id, ch_name):
        pd = ProviderDal()
        provModel = pd.get_prov_by_id_and_at(asset_type_id, ch_name)
        return self.actual_return_id_val(provModel)

    def get_model_id_by_pd_ch(self, prov_id, ch_name):
        md = ModelDal()
        model = md.get_model_by_pd_ch(prov_id, ch_name)
        return self.actual_return_id_val(model)

    # TODO 将这几个抽象出来 在table和model映射的时候
    def get_device_state_id_by_ch_name(self, ch_name):
        dse = DeviceStateDal()
        device_state = dse.get_device_state_id_by_ch_name(ch_name)
        return self.actual_return_id_val(device_state)

    def get_store_state_id_by_ch_name(self, ch_name):
        ste = StoreStateDal()
        store_state = ste.get_store_state_id_by_ch_name(ch_name)
        return self.actual_return_id_val(store_state)

    def get_store_place_id_by_ch_name(self, ch_name):
        spe = StorePlaceDal()
        store_place = spe.get_store_place_id_by_ch_name(ch_name)
        return self.actual_return_id_val(store_place)

    def get_in_out_reason_id_by_ch_name(self, ch_name):
        ion = InOutReasonDal()
        in_out_reason = ion.get_reason_id_by_ch_name(ch_name)
        return self.actual_return_id_val(in_out_reason)

    def actual_return_id_val(self, actual_model):
        if actual_model is not None:
            return actual_model.id
        return ''

    def get_model_id_by_asset_type_pd(self, asset_type_id, provider, model):
        prov_id = self.get_prov_id_by_atd_ch(asset_type_id, provider)
        model_id = self.get_model_id_by_pd_ch(prov_id, model)
        return model_id

    def get_asset_type_and_model_id(self, params):
        asset_type_id = self.get_id_by_at_asset_ch_name(params['asset_type'])
        prov_id = self.get_prov_id_by_atd_ch(asset_type_id, params['provider'])
        model_id = self.get_model_id_by_pd_ch(prov_id, params['model'])
        return [asset_type_id, model_id]