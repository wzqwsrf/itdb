# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import json

from flask import (
    Blueprint,
    render_template,
    request,
)
from qg.core import log as logging
from itdblib.services.attribute_manager_service import AttributeManagerService
from itdblib.common import ajax

LOG = logging.getLogger(__name__)

bp = Blueprint('attribute_manager', __name__)


@bp.route('/attribute_manager', methods=['GET', 'POST'])
def attributeManager():
    return render_template('attribute_manager.html', pageTitle=u'设备管理')


@bp.route('/load_device_type_lists', methods=['POST', 'GET'])
def deviceTypeLists():
    deviceList = []
    try:
        deviceList = AttributeManagerService().get_all_devices()
        return json.dumps(deviceList)
    except Exception, _ex:
        LOG.error("get all device provider model is error: %s"
                 % str(_ex))
        return json.dumps(deviceList)


@bp.route('/add_device_type', methods=['POST'])
def addDeviceType():
    try:
        data = request.form
        dataNew = {}
        for k, v in data.items():
            dataNew[k] = v
        bFlag, strRet = AttributeManagerService().addDeviceTypeInfos(dataNew)
        if bFlag:
            return ajax.api_success(msg=strRet, data=[])
        else:
            return ajax.api_error(msg=strRet)
    except Exception, _ex:
        LOG.error("error occured while add device type: %s" % str(_ex))
        return ajax.api_error(msg=u'添加失败')


@bp.route('/add_asset_class_infos', methods=['POST'])
def addAssetClass():
    try:
        data = request.form
        dataNew = {}
        for k, v in data.items():
            dataNew[k] = v
        num, msg = AttributeManagerService().addAssetClass(dataNew)
        if -1 == num:
            LOG.error("添加错误")
            return ajax.api_error(msg=msg)
        elif 0 == num:
            return ajax.api_success(msg=msg, data=False)
        else:
            return ajax.api_success(msg=msg)
    except Exception as _ex:
        LOG.error("error occured while add asset tree node: %s" % str(_ex))
        return ajax.api_error(msg=u'添加失败')


@bp.route('/remove_asset_class_node', methods=['POST'])
def removeAssetClassNode():
    try:
        data = request.form
        dataNew = {}
        for k, v in data.items():
            dataNew[k] = v
        bFlag = AttributeManagerService().removeAssetClassNode(dataNew)
        if bFlag:
            return ajax.api_error(msg=u'删除失败')
        return ajax.api_success(msg=u"删除成功", data=[])
    except Exception as _ex:
        LOG.error("error occured while remvoe asset tree node: %s" % str(_ex))
        return ajax.api_error(msg=u'删除失败')


@bp.route('/load_store_house_infos', methods=['POST', 'GET'])
def loadStoreHouseInfos():
    storeList = []
    try:
        storeList = AttributeManagerService().get_all_store_place_infos()
        return json.dumps(storeList)
    except Exception, _ex:
        LOG.error("get all storehouse infos is error: %s"
                 % str(_ex))
        return json.dumps(storeList)


@bp.route('/add_store_place', methods=['POST'])
def addStorehouseMsgs():
    try:
        data = request.form
        print data
        bFlag, msg = AttributeManagerService().addStorePlace(data)
        if bFlag:
            return ajax.api_success(msg=msg, data=[])
        else:
            return ajax.api_error(msg=msg)
    except Exception as _ex:
        LOG.error("error occured while add storehouse msgs: %s" % str(_ex))
        return ajax.api_error(msg=u'添加失败')
