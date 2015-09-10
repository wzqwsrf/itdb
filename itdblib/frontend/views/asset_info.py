# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from flask import (
    Blueprint,
    request,
    session
)
import json
from itdblib.services.construct_dict_service import ConstructDictService
from itdblib.services.asset_info_service import AssetInfoService
from itdblib.services.asset_phone_service import AssetPhoneService
from itdblib.services.asset_consume_service import AssetConsumeService
from qg.core import log as logging
from itdblib.common import ajax

LOG = logging.getLogger(__name__)

bp = Blueprint('asset_info', __name__)


@bp.route('/asset/id', methods=['POST'])
def show_asset_info_by_id():
    search_val = request.form["return_val"]
    ais = AssetInfoService()
    return ais.get_asset_info_show(search_val)


@bp.route('/loadstate/1', methods=['GET'])
def load_device_state_list():
    return ConstructDictService().get_device_state_list()


@bp.route('/loadstate/2', methods=['GET'])
def load_store_state_list():
    return ConstructDictService().get_store_state_list()


@bp.route('/loadstate/3', methods=['GET'])
def load_store_place_list():
    return ConstructDictService().get_store_place_list()


@bp.route('/loadstate/4', methods=['GET'])
def load_in_reason_list():
    return ConstructDictService().get_in_reason_list()


@bp.route('/loadstate/5', methods=['GET'])
def load_out_reason_list():
    return ConstructDictService().get_out_reason_list()


@bp.route('/prov/types', methods=['POST'])
def get_prov_type_list():
    asset_type = request.form['return_val']
    prov_list = AssetInfoService().get_prov_list_by_type(asset_type)
    return json.dumps(prov_list)


@bp.route('/model/types', methods=['POST'])
def get_model_type_list():
    model_list = []
    try:
        asset_type = request.form['return_val']
        asset_msg = asset_type.split('_')
        if asset_msg[0] is not None and asset_msg[1] is not None:
            model_list = AssetInfoService().get_model_by_prov(
                            asset_msg[0], asset_msg[1])
        return json.dumps(model_list)
    except Exception as _ex:
        LOG.error("error occured while get_model_type_list : %s" % str(_ex))
        return json.dumps(model_list)


@bp.route('/owner', methods=['POST'])
def get_owner_by_rtx_id():
    rtx_id = request.form['return_val']
    owner = AssetInfoService().get_owner_by_rtx_id(rtx_id)
    return json.dumps({'owner': owner})


@bp.route('/old/add', methods=['POST'])
def store_old_add_store():
    data = request.form
    ret, msg = AssetInfoService().store_old_add_data(data)
    if ret:
        LOG.info(msg)
        return ajax.api_success(msg=msg, data=[])
    else:
        LOG.error(msg)
        return ajax.api_error(msg=msg)


@bp.route('/auto/show', methods=['POST'])
def get_info_by_input():
    rtx_id = request.form['return_val']
    result = AssetInfoService().get_employee_by_input(rtx_id)
    return json.dumps(result)


@bp.route('/save_oper', methods=['POST'])
def save_operation_info():
    try:
        params = request.form
        data = {}
        for k, v in params.items():
            data[k] = v
        print params
        data['operator'] = session.get('rtx_id')
        ais = AssetInfoService()
        ais.save_oper_info(data)
    except Exception, _ex:
        LOG.error("error occured while save_oper_info : %s" % str(_ex))
        return u"保存失败"
    return u"保存成功"


@bp.route('/phone/id', methods=['POST'])
def show_asset_phone_info_by_id():
    search_val = request.form["return_val"]
    aps = AssetPhoneService()
    return aps.get_asset_phone_info_by_id(search_val)


@bp.route('/consume/id', methods=['POST'])
def show_asset_consume_info_by_id():
    search_val = request.form["return_val"]
    acs = AssetConsumeService()
    return acs.get_asset_consume_info_by_rtx_id(search_val)


@bp.route('/auto/id', methods=['POST'])
def auto_asset_info_by_id():
    search_val = request.form["return_val"]
    ais = AssetInfoService()
    params = ais.get_asset_info_three_info_by_id(search_val)
    return json.dumps(params)


@bp.route('/admin/name', methods=['POST'])
def show_admin_name_by_store_place():
    search_val = request.form["return_val"]
    ais = AssetInfoService()
    return ais.get_admin_name_by_store_place(search_val)