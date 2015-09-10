# -*- coding: utf-8 -*-
#
# Copyright @ 2014 OPS, Qunar Inc. (qunar.com)
#
# Author: zhenqing.wang <zhenqing.wang@qunar.com>
#

from flask import (
    request,
    Blueprint,
    session,
    render_template,
    make_response,
    send_file
)
from qg.core import log as logging
from itdblib.common import ajax
from itdblib.services.asset_phone_service import AssetPhoneService
from itdblib.dal.asset_phone_info_dal import AssetPhoneInfoDal
from itdblib.common.asset_info_utils import AssetInfoUtils

import os

LOG = logging.getLogger(__name__)

bp = Blueprint('asset_phone', __name__)


@bp.route('/asset/phone', methods=['POST'])
def show_asset_phone_info():
    start = request.form['iDisplayStart']
    count = request.form['iDisplayLength']
    aps = AssetPhoneService()
    return aps.get_asset_phone_info_all_show(start, count)


@bp.route('/asset_phone', methods=['GET', 'POST'])
def assetPhone():
    return render_template('asset_phone.html', pageTitle=u'号码管理')


@bp.route('/phone/<id>', methods=['POST'])
def show_asset_phone_info_by_all(id):
    start = request.values['iDisplayStart']
    count = request.values['iDisplayLength']
    aps = AssetPhoneService()
    return aps.get_asset_phone_info_search_show(id, start, count)


@bp.route('/phone/id/<phone_no>', methods=['GET'])
def show_asset_phone_info_by_id(phone_no):
    aps = AssetPhoneService()
    return aps.get_asset_phone_info_by_id(phone_no)


@bp.route('/operate/<phone_no>', methods=['GET'])
def get_operate_infos(phone_no):
    from itdblib.dal.operation_info_dal import OperationInfoDal

    operInfos = OperationInfoDal().get_all_oper_info_by_asset_id(phone_no)
    aps = AssetPhoneService()
    return aps.get_phone_operate_json(operInfos)


@bp.route('/phone/advanced', methods=['POST'])
def show_advanced_asset_info():
    start = request.values['iDisplayStart']
    count = request.values['iDisplayLength']
    aps = AssetPhoneService()
    params = request.values
    return aps.get_asset_phone_info_advanced_search_show(params, start, count)


@bp.route('/old/add', methods=['POST'])
def store_phone_old_data():
    data = request.form
    print data
    ret, msg = AssetPhoneService().store_phone_old_add_data(data)
    if ret:
        LOG.info(msg)
        return ajax.api_success(msg=msg, data=[])
    else:
        LOG.error(msg)
        return ajax.api_error(msg=msg)


@bp.route('/out', methods=['POST'])
def get_required_out_data():
    data = request.form
    return AssetPhoneService().get_phone_out_data(data)


@bp.route('/out/data', methods=['POST'])
def store_phone_out_data():
    data = request.form
    operator = session.get('rtx_id')
    ret, msg = AssetPhoneService().store_phone_out_data(data, operator)
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
    chlist = aiu.output_phone_excel_ch_list()
    enlist = aiu.output_phone_excel_en_list()
    params = AssetPhoneService().get_export_excel_data(key)
    save_file = writeExcel(params, '电话号码类结果数据.xls', chlist, enlist)
    response = make_response(send_file(save_file,
                                       as_attachment=True
                            ))
    filesize = os.path.getsize(save_file)
    response.headers['Content-Length'] = filesize
    os.remove(save_file)
    return response
