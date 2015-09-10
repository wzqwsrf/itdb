# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from flask import (
    request,
    Blueprint,
    render_template,
    send_file,
    session,
    make_response
)
import os
from qg.core import log as logging
from itdblib.common import ajax
from itdblib.services.asset_consume_service import AssetConsumeService
from itdblib.common.asset_info_utils import AssetInfoUtils

LOG = logging.getLogger(__name__)

bp = Blueprint('asset_consume', __name__)


@bp.route('/asset/consume', methods=['POST'])
def show_asset_info():
    start = request.form['iDisplayStart']
    count = request.form['iDisplayLength']
    acs = AssetConsumeService()
    return acs.get_asset_consume_info_all_show(start, count)


@bp.route('/asset_consume', methods=['GET', 'POST'])
def assetConsume():
    return render_template('asset_consume.html', pageTitle=u'耗材管理')


@bp.route('/consume/num', methods=['POST'])
def get_consume_num():
    params = request.form
    acs = AssetConsumeService()
    return acs.get_prov_model_place_num(params)


@bp.route('/consume/<id>', methods=['POST'])
def show_asset_phone_info_by_all(id):
    start = request.values['iDisplayStart']
    count = request.values['iDisplayLength']
    acs = AssetConsumeService()
    return acs.get_asset_consume_info_search_show(id, start, count)


@bp.route('/operate/<consume_id>', methods=['GET'])
def get_operate_infos(consume_id):
    from itdblib.dal.operation_info_dal import OperationInfoDal

    operInfos = OperationInfoDal().get_all_oper_info_by_asset_id(consume_id)
    aps = AssetConsumeService()
    return aps.get_consume_operate_json(operInfos)


@bp.route('/consume/id/<consume_id>', methods=['GET'])
def show_asset_consume_info_by_id(consume_id):
    acs = AssetConsumeService()
    return acs.get_asset_consume_info_by_id(consume_id)


@bp.route('/consume/out', methods=['POST'])
def add_old_asset_info():
    params = request.form
    operator = session.get('rtx_id')
    ret = AssetConsumeService().store_out_add_consume_data(params, operator)
    if ret:
        msg = u"已有耗材类数据出库成功"
        LOG.info(msg)
        return ajax.api_success(msg=msg, data=[])
    else:
        msg = u"已有耗材类数据出库失败"
        LOG.error(msg)
        return ajax.api_error(msg=msg)


@bp.route('/consume/advanced', methods=['POST'])
def show_advanced_asset_info():
    start = request.values['iDisplayStart']
    count = request.values['iDisplayLength']
    acs = AssetConsumeService()
    params = request.values
    return acs.get_asset_consume_info_advanced_search_show(params, start, count)


@bp.route('/old/add', methods=['POST'])
def store_consume_old_data():
    data = request.form
    ret, msg = AssetConsumeService().store_consume_old_add_data(data)
    if ret:
        LOG.info(msg)
        return ajax.api_success(msg=msg, data=[])
    else:
        LOG.error(msg)
        return ajax.api_error(msg=msg)


@bp.route('/export/asset', methods=['POST', 'GET'])
def export_asset_info():
    key = request.form['exportData']
    from itdblib.common.xls_utils import writeExcel

    aiu = AssetInfoUtils()
    chlist = aiu.output_consume_excel_ch_list()
    enlist = aiu.output_consume_excel_en_list()
    params = AssetConsumeService().get_export_excel_data(key)
    save_file = writeExcel(params, '耗材类结果数据.xls', chlist, enlist)
    response = make_response(send_file(save_file,
                                       as_attachment=True
                                       ))
    filesize = os.path.getsize(save_file)
    response.headers['Content-Length'] = filesize
    os.remove(save_file)
    return response
