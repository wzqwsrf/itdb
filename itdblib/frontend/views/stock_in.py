# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import os
import json

from flask import (
    Blueprint,
    render_template,
    request,
    session
)
from werkzeug.utils import secure_filename
from qg.core import log as logging

from itdblib.common.parse_excel import get_excel_sheet_name
from itdblib.common import ajax
from itdblib.services.stock_in_service import StockInService
from itdblib.services.asset_consume_service import AssetConsumeService

LOG = logging.getLogger(__name__)

bp = Blueprint('stock_in', __name__)

@bp.route('/stock_in', methods=['GET', 'POST'])
def stockIn():
    return render_template('stock_in.html', pageTitle=u'入库')


@bp.route('/asset/types', methods=['POST'])
def get_asset_type_list():
    num = request.form['return_val']
    num = int(num)
    return StockInService().get_asset_type_list(num)


@bp.route('/new/add', methods=['POST'])
def add_new_asset_info():
    # try:
    data = request.form
    sis = StockInService()
    new_data = {}
    for k, v in data.items():
        new_data[k] = v
    ret, msg = sis.add_new_asset_info(new_data)
    return json.dumps(dict(msg=msg, success=ret))
    # if ret:
    # return ajax.api_success(msg=u'添加成功', data=[])
    # else:
    # LOG.error(msg)
    # return ajax.api_error(msg=msg)
    # except Exception as _ex:
    #     LOG.error("error occured while add_new_asset_info : %s" % str(_ex))
    #     return ajax.api_error(msg=u'添加失败')


@bp.route('/upload_asset_file', methods=['POST'])
def upload_asset_file():
    try:
        f = request.files.get("file")
        if not f:
            return ajax.api_error(msg=u'没有获取文件信息')
        fileName = secure_filename(f.filename)
        path = '/tmp/'
        fileFullPath = os.path.join(path, fileName)
        # import re
        # temp = tempfile.mkdtemp(suffix='xlsx', prefix='asset', dir=fileFullPath)
        # os.rename(os.path.join(path, fileName), os.path.join(path, new_name))
        f.save(fileFullPath)
        ret, msg = get_excel_sheet_name(fileFullPath)
        if not ret:
            return ajax.api_error(msg=msg)
        else:
            operator = session.get('rtx_id')
            ss = StockInService()
            ret, msg = ss.muti_stock_in_different_assets(fileFullPath, operator, int(msg))
            if ret:
                return ajax.api_success(msg=msg, data=[])
            else:
                return ajax.api_error(msg=msg)
    except Exception, _ex:
        LOG.error("error occured while upload_asset_file : %s" % str(_ex))
        return ajax.api_error(msg=u'添加失败')


@bp.route('/consume/num', methods=['POST'])
def get_consume_num():
    params = request.form
    acs = AssetConsumeService()
    return str(acs.get_prov_model_place_num(params))


@bp.route('/consume/use_num', methods=['POST'])
def get_consume_in_num():
    params = request.form
    acs = AssetConsumeService()
    params = acs.get_prov_model_user_name_num(params)
    return params