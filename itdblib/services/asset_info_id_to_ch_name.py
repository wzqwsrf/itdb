# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from qg.core import log as logging
from itdblib.dal.asset_type_dal import AssetTypeDal
from itdblib.dal.device_state_dal import DeviceStateDal
from itdblib.dal.store_state_dal import StoreStateDal
from itdblib.dal.store_place_dal import StorePlaceDal
from itdblib.dal.in_out_reason_dal import InOutReasonDal
from itdblib.common.time_utils import trans_time
from itdblib.common.corehr_api_utils import get_employee_owner
from itdblib.common.asset_info_utils import AssetInfoUtils
from itdblib.dal.operation_info_dal import OperationInfoDal
from itdblib.dal.provider_dal import ProviderDal
from itdblib.dal.model_dal import ModelDal
LOG = logging.getLogger(__name__)


class AssetInfoIdToChName():

    def get_asset_manager_show_info(self, assetInfo):
        params = {}
        if assetInfo is None:
            return params
        params['asset_id'] = assetInfo.asset_id
        params['asset_type'] = self.get_asset_type_name_by_num(assetInfo.asset_type_id)
        params['sn'] = assetInfo.sn
        params['device_state'] = self.get_device_state_name_by_num(
                                        assetInfo.device_state_id)
        params['user_name'] = assetInfo.user_name
        params['store_state'] = self.get_store_state_name_by_num(
                                        assetInfo.store_state_id)
        return params

    def get_detail_asset_info(self, assetInfo):
        params = self.get_excel_asset_info(assetInfo)
        params['owner'] = get_employee_owner(assetInfo.user_name)
        operInfo = OperationInfoDal().get_oper_info_by_asset_id(assetInfo.asset_id)
        params['operator'] = '' if not operInfo\
                            else operInfo['operator']
        return params

    def get_excel_asset_info(self, assetInfo):
        params = self.get_asset_manager_show_info(assetInfo)
        model_id = assetInfo.model_id
        params['model'] = self.get_model_name_by_num(model_id)
        params['provider'] = self.get_prov_name_by_num(assetInfo.asset_type_id, model_id)
        params['in_out_reason'] = self.get_in_out_reason_name_by_num(
                                        assetInfo.in_out_reason_id)
        params['store_place'] = self.get_store_place_name_by_num(
                                        assetInfo.store_place_id)
        params['create_time'] = trans_time(assetInfo.create_time)
        params['update_time'] = trans_time(assetInfo.update_time)
        params['up_time'] = trans_time(assetInfo.up_time)
        params['remark'] = assetInfo.remark
        params['type_info'] = str(assetInfo.type_info)
        params = self.format_type_info(params, assetInfo.type_info)
        return params

    def get_asset_type_name_by_num(self, asset_type_id):
        atd = AssetTypeDal()
        assetType = atd.get_asset_type_name_by_id(asset_type_id)
        return self.actual_return_ch_name_val(assetType)

    def get_device_state_name_by_num(self, device_state_id):
        dse = DeviceStateDal()
        device_state = dse.get_device_state_name_by_id(device_state_id)
        return self.actual_return_ch_name_val(device_state)

    def get_store_state_name_by_num(self, store_state_id):
        ste = StoreStateDal()
        store_state = ste.get_store_state_name_by_id(store_state_id)
        return self.actual_return_ch_name_val(store_state)

    def get_store_place_name_by_num(self, store_place_id):
        spe = StorePlaceDal()
        store_place = spe.get_store_place_name_by_id(store_place_id)
        return self.actual_return_ch_name_val(store_place)

    def get_in_out_reason_name_by_num(self, in_out_reason_id):
        ion = InOutReasonDal()
        in_out_reason = ion.get_reason_name_by_id(in_out_reason_id)
        return self.actual_return_ch_name_val(in_out_reason)

    def get_model_by_num(self, model_id):
        md = ModelDal()
        model = md.get_model_name_by_id(model_id)
        return model

    def get_model_name_by_num(self, model_id):
        md = ModelDal()
        model = md.get_model_name_by_id(model_id)
        return self.actual_return_name_val(model)

    def get_prov_name_by_atd_md_num(self, asset_type_id, prov_id):
        pd = ProviderDal()
        provModel = pd.get_prov_name_by_atd_md(asset_type_id, prov_id)
        return self.actual_return_name_val(provModel)

    def get_prov_name_by_num(self, asset_type_id, model_id):
        model = self.get_model_by_num(model_id)
        return self.get_prov_name_by_atd_md_num(asset_type_id, model.provider_id)

    def actual_return_ch_name_val(self, actual_model):
        if actual_model is not None:
            return actual_model.ch_name
        return ''

    def actual_return_name_val(self, actual_model):
        if actual_model is not None:
            return actual_model.name
        return ''

    def format_type_info(self, params, type_info):
        field = type_info
        if field:
            for k, v in field.items():
                if k and v:
                    params[k] = v
        return params


