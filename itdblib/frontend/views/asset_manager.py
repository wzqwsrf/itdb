# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from flask import (
    Blueprint,
    render_template,
    request,
    send_file,
    make_response
)
from qg.core import log as logging
import os
from itdblib.services.asset_manager_service import AssetManagerService
from itdblib.services.asset_info_service import AssetInfoService
from itdblib.common import ajax
from itdblib.dal.asset_info_dal import AssetInfoDal
from itdblib.common.asset_info_utils import AssetInfoUtils

LOG = logging.getLogger(__name__)

bp = Blueprint('asset_manager', __name__)


@bp.route('/asset_manager', methods=['GET'])
def assetManager():
    return render_template("asset_manager.html", pageTitle=u'资产管理')


@bp.route('/asset', methods=['POST'])
def show_asset_info():
    start = request.form['iDisplayStart']
    count = request.form['iDisplayLength']
    print request.form
    ams = AssetManagerService()
    return ams.get_asset_info_all_show(start, count)


@bp.route('/asset/<id>', methods=['POST'])
def show_asset_info_by_all(id):
    start = request.values['iDisplayStart']
    count = request.values['iDisplayLength']
    ams = AssetManagerService()
    return ams.get_asset_info_search_show(id, start, count)


@bp.route('/asset/advanced', methods=['POST'])
def show_advanced_asset_info():
    start = request.values['iDisplayStart']
    count = request.values['iDisplayLength']
    ams = AssetManagerService()
    params = request.values
    return ams.get_asset_info_advanced_search_show(params, start, count)


@bp.route('/asset/id/<asset_id>', methods=['GET'])
def show_asset_info_by_id(asset_id):
    ais = AssetManagerService()
    return ais.get_asset_info_by_asset_id(asset_id)


@bp.route('/operate/<asset_id>', methods=['GET'])
def get_operate_infos(asset_id):
    from itdblib.dal.operation_info_dal import OperationInfoDal

    operInfos = OperationInfoDal().get_all_oper_info_by_asset_id(asset_id)
    ams = AssetManagerService()
    return ams.get_asset_operate_json(operInfos)


@bp.route('/edit_asset', methods=['POST'])
def submit_asset_info():
    try:
        params = request.form
        ams = AssetManagerService()
        ret, msg = ams.store_edit_asset_info_data(params)
        if ret:
            LOG.info(msg)
            return ajax.api_success(msg=msg, data=[])
        else:
            LOG.error(msg)
            return ajax.api_error(msg=msg)
    except Exception, _ex:
        LOG.error("error occured while submit_asset_info : %s" % str(_ex))
        return u"编辑失败"


@bp.route('/export/asset', methods=['POST', 'GET'])
def export_asset_info():
    key = request.form['exportData']
    from itdblib.common.xls_utils import writeExcel

    aiu = AssetInfoUtils()
    chlist = aiu.output_excel_ch_list()
    enlist = aiu.output_excel_en_list()
    params = AssetManagerService().get_export_excel_data(key)
    save_file = writeExcel(params, '固定资产类结果数据.xls', chlist, enlist)
    response = make_response(send_file(save_file,
                                       as_attachment=True
                            ))
    filesize = os.path.getsize(save_file)
    response.headers['Content-Length'] = filesize
    os.remove(save_file)
    return response
