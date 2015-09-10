# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import json
from itdblib.common.time_utils import trans_time
from itdblib.dal.operation_info_dal import OperationInfoDal
from itdblib.common.asset_info_utils import AssetInfoUtils
from itdblib.common.time_utils import get_now_date
from itdblib.common.type_info_utils import (
    wireList,
    vpnList,
    macList,
    type_info_en_list,
    assetInfoMacEnlist,
    assetInfoVpnEnlist,
    assetInfoWireEnlist
)
from qg.core import log as logging

LOG = logging.getLogger(__name__)


class AssetOperateService():
    def __init__(self):
        LOG.info('init AssetOperateService!')

    def get_operate_json(self, operInfos, en_ch_dict):
        ret = []
        for operInfo in operInfos:
            params = {}
            params['oper_time'] = trans_time(operInfo.oper_time)
            params['oper_type'] = operInfo.oper_type
            params['operator'] = operInfo.operator
            params['text'] = operInfo.text
            params['before_field'] = self.format_hstore_val(
                operInfo.before_field, en_ch_dict)
            params['after_field'] = self.format_hstore_val(
                operInfo.after_field, en_ch_dict)
            ret.append(params)
        return json.dumps(ret)

    def format_hstore_val(self, field, en_ch_dict):
        if not field and field is None or field == '' or len(field) == 0:
            return ''
        ret = []
        for k, v in field.items():
            ret.append("".join([en_ch_dict.get(k), ":", v]))
        return ",".join(ret)

    def construct_and_add_batch_operate_info(self, params, rtx_id):
        operInfos = []
        for param in params:
            asset_type = param['asset_type']
            operInfo = {}
            before_field = {}
            after_field = {}
            excel_en_list = AssetInfoUtils().input_excel_en_list()
            flag = False
            for name in excel_en_list:
                if asset_type in macList():  # 记录MAC地址
                    if name in set(type_info_en_list()).difference(set(assetInfoMacEnlist())):
                        continue
                elif asset_type in vpnList():
                    if name in set(type_info_en_list()).difference(set(assetInfoVpnEnlist())):
                        continue
                elif asset_type in wireList():
                    if name in set(type_info_en_list()).difference(set(assetInfoWireEnlist())):
                        continue
                else:
                    if name in type_info_en_list():
                        continue
                before_field[name] = ''
                after_field[name] = param[name]
            operInfo['before_field'] = before_field
            operInfo['after_field'] = after_field
            operInfo['asset_id'] = param['asset_id']
            operInfo['oper_type'] = '批量入库'
            operInfo['operator'] = rtx_id
            operInfo['text'] = ''
            operInfo['oper_time'] = get_now_date()
            operInfos.append(operInfo)
        OperationInfoDal().add_batch_oper_infos(operInfos)

    def construct_and_add_phone_batch_operate_info(self, params, rtx_id):
        operInfos = []
        for param in params:
            operInfo = {}
            before_field = {}
            after_field = {}
            excel_en_list = AssetInfoUtils().input_phone_excel_en_list()
            flag = False
            for name in excel_en_list:
                before_field[name] = ''
                after_field[name] = param[name]
            operInfo['before_field'] = before_field
            operInfo['after_field'] = after_field
            operInfo['asset_id'] = param['phone_no']
            operInfo['oper_type'] = '批量入库'
            operInfo['operator'] = rtx_id
            operInfo['text'] = ''
            operInfo['oper_time'] = get_now_date()
            operInfos.append(operInfo)
        OperationInfoDal().add_batch_oper_infos(operInfos)

