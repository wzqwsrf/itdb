# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import json
from itdblib.dal.asset_info_dal import AssetInfoDal
from itdblib.dal.provider_dal import ProviderDal
from itdblib.services.asset_info_id_to_ch_name import AssetInfoIdToChName
from itdblib.services.asset_info_ch_name_to_id import AssetInfoChNameToId
from itdblib.services.construct_dict_service import ConstructDictService
from itdblib.services.asset_operate_service import AssetOperateService
from itdblib.services.asset_info_service import AssetInfoService
from itdblib.common.asset_info_utils import AssetInfoUtils
from itdblib.common.corehr_api_utils import get_actual_rtx_id
from qg.core import log as logging

LOG = logging.getLogger(__name__)


class AssetManagerService():
    def __init__(self):
        LOG.info('init AssetManagerService!')

    def get_asset_info_all_show(self, start, count):
        assetInfos = AssetInfoDal().get_asset_info_limit(start, count)
        count = AssetInfoDal().get_asset_info_num()
        return self.get_asset_info_all(assetInfos, count)

    def get_asset_info_all(self, assetInfos, count):
        aic = AssetInfoIdToChName()
        ret = []
        for assetInfo in assetInfos:
            params = aic.get_asset_manager_show_info(assetInfo)
            ret.append(params)
        rets = {'data': ret, 'count': count}
        return json.dumps(rets)

    def get_asset_info_search_show(self, id, start, count):
        rtx_id = get_actual_rtx_id(id)
        assetInfos = AssetInfoDal(). \
            get_asset_info_by_search_val_all(rtx_id, start, count)
        count = self.get_asset_infos_num_by_search_val(rtx_id)
        return self.get_asset_info_all(assetInfos, count)

    def get_asset_infos_num_by_search_val(self, id):
        rtx_id = get_actual_rtx_id(id)
        return AssetInfoDal().get_asset_info_query_num(rtx_id)

    def get_asset_operate_json(self, operInfos):
        aos = AssetOperateService()
        en_ch_dict = self.get_asset_en_ch_dict()
        return aos.get_operate_json(operInfos, en_ch_dict)

    def get_prov_list_by_atd(self, asset_type_id):
        pd = ProviderDal()
        return pd.get_prov_by_asset_type(asset_type_id)

    def get_actual_prov_list(self, asset_type):
        aoc = AssetInfoChNameToId()
        id = aoc.get_id_by_at_asset_ch_name(asset_type)
        return self.get_prov_list_by_atd(id)

    def store_edit_asset_info_data(self, params):
        data = {}
        for k, v in params.items():
            data[k] = v
        cds = ConstructDictService()
        data['type_info'] = cds.construct_type_info(data)
        aoc = AssetInfoChNameToId()
        new_data = aoc.trans_ch_data_to_id(data)
        ret, msg = AssetInfoDal().edit_asset_info(new_data)
        return ret, msg

    def get_asset_info_advanced_search_show(self, request_params, start, count):
        ais = AssetInfoService()
        params = ais.get_advanced_web_params(request_params)
        return self.get_advanced_search_val_all(params, start, count)

    def get_advanced_search_val_all(self, params, start, count):
        aid = AssetInfoDal()
        assetInfos = aid.get_advanced_search_val_limit(params, start, count)
        count = aid.get_advanced_search_val_count(params)
        return self.get_asset_info_all(assetInfos, count)

    def get_export_excel_data(self, key):
        if key != "":
            # 传递过来的值包含=，是高级查询
            if key.find("=") >= 0:
                ais = AssetInfoService()
                params = ais.get_data_by_split_web(key)
                params = ais.get_advanced_web_params(params)
                assetInfos = AssetInfoDal().get_advanced_search_val_all_datas(params)
            # 一般查询
            else:
                rtx_id = get_actual_rtx_id(key)
                assetInfos = AssetInfoDal().get_asset_info_excel_by_search_val_all(rtx_id)
        else:
            assetInfos = AssetInfoDal().get_asset_info_all()

        ret = []
        aoc = AssetInfoIdToChName()
        for assetInfo in assetInfos:
            params = aoc.get_excel_asset_info(assetInfo)
            ret.append(params)
        return ret

    def get_detail_asset_info_all(self, assetInfos, count):
        aic = AssetInfoIdToChName()
        ret = []
        for assetInfo in assetInfos:
            params = aic.get_excel_asset_info(assetInfo)
            ret.append(params)
        rets = {'data': ret, 'count': count}
        return json.dumps(rets)

    def get_asset_en_ch_dict(self):
        aiu = AssetInfoUtils()
        enlist = aiu.get_asset_info_en_list()
        chlist = aiu.get_asset_info_ch_list()
        d_len = len(enlist)
        return dict([(enlist[i], chlist[i]) for i in range(d_len)])

    def get_asset_info_by_asset_id(self, asset_id):
        assetInfo = AssetInfoDal().get_asset_info_by_id(asset_id)
        if assetInfo is None:
            return ''
        aic = AssetInfoIdToChName()
        ret = []
        params = aic.get_detail_asset_info(assetInfo)
        ret.append(params)
        return json.dumps(ret)