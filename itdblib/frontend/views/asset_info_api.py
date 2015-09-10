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

bp = Blueprint('asset', __name__)


@bp.route('/', methods=['GET'])
def assetManager():
    return render_template("blank.html")

@bp.route('/<rtx_id>', methods=['GET'])
def show_asset_info_by_rtx_id(rtx_id):
    assetInfos = AssetInfoDal().get_asset_info_by_user_name(rtx_id)
    ams = AssetManagerService()
    return ams.get_detail_asset_info_all(assetInfos, len(assetInfos))
