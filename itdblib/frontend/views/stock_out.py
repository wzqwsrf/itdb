# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from flask import (
    request,
    Blueprint,
    render_template
)
from qg.core import log as logging
from itdblib.common import ajax
from itdblib.services.stock_out_service import StockOutService

LOG = logging.getLogger(__name__)

bp = Blueprint('stock_out', __name__)


@bp.route('/stock_out', methods=['GET', 'POST'])
def stockOut():
    return render_template('stock_out.html', pageTitle=u'出库')


@bp.route('/update_stock_outing_state', methods=['POST'])
def updateStockOutInfos():
    try:
        data = request.form
        dataNew = {}
        for k, v in data.items():
            dataNew[k] = v
        bRet, msg = StockOutService().updateStockOutInfos(dataNew)
        if not bRet:
            return ajax.api_error(msg=msg)
        else:
            return ajax.api_success(msg=u'出库成功', data=[])
    except Exception as _ex:
        LOG.error("error occured while modify stock out asset infos: %s"
                  % str(_ex))
        return ajax.api_error(msg=u'出库失败')
