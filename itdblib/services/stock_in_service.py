# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import json
import copy

from qg.core import log as logging

from itdblib.services.asset_info_service import AssetInfoService
from itdblib.services.construct_dict_service import ConstructDictService
from itdblib.services.asset_operate_service import AssetOperateService
from itdblib.dal.asset_type_dal import AssetTypeDal
from itdblib.dal.asset_info_dal import AssetInfoDal
from itdblib.dal.operation_info_dal import OperationInfoDal
from itdblib.dal.asset_phone_info_dal import AssetPhoneInfoDal
from itdblib.common.time_utils import get_now_date
from itdblib.common.parse_excel import data_set_from_excel, get_phone_data_set_from_excel
from itdblib.dal.asset_phone_info_dal import AssetPhoneInfoDal
from itdblib.services.asset_info_ch_name_to_id import AssetInfoChNameToId
from itdblib.services.asset_consume_service import AssetConsumeService

LOG = logging.getLogger(__name__)


class StockInService:
    def __init__(self):
        LOG.info('init StockInService!')

    def get_asset_type_list(self, num):
        asset_type_list = []
        try:
            if num == 1:  # 查询固定资产 无线资产
                asset_types = AssetTypeDal().search_by_path('it.gz.*')
                asset_types1 = AssetTypeDal().search_by_path('it.wireless.*')
                asset_types += asset_types1
            elif num == 2:  # 查询耗材
                asset_types = AssetTypeDal().search_by_path('it.consume.*')
            elif num == 3:
                asset_types = AssetTypeDal().search_by_path('it.phoneno.*')
            else:
                asset_types = AssetTypeDal().get_asset_type_all()
            for asset_type in asset_types:
                temp_dict = {}
                temp_dict[asset_type.asset_path] = asset_type.ch_name
                asset_type_list.append(temp_dict)
            ret_list = self.ltree_to_ztree(asset_type_list)
            return json.dumps(ret_list)
        except Exception as _ex:
            LOG.error("error occured while get type list : %s" % str(_ex))
            return json.dumps(asset_type_list)

    def ltree_to_ztree(self, typeList):
        """ 将ltree型数据转化成ztree格式
        """
        # 得到所有的ltree path列表
        totalList = []
        for item in typeList:
            for key in item.keys():
                totalList.append(key)

        # 将ltree path 分割
        levelList = []
        for item in totalList:
            tempList = item.split(".")
            levelList.append(tempList)

        # 得到ltree最深的级别
        nMax = 0
        nLen = 0
        for item in levelList:
            nLen = len(item)
            if nMax < nLen:
                nMax = nLen

        # 得到每一级对应的节点，根节点对应第0级，依次往下
        # 0 : ['it']
        # 1 : ['gz', 'wireless', 'pj']
        # 2 : ['laptop', 'desktop', screen']
        tempDict = {}
        for i in xrange(nMax):
            tempSet = set()
            for item in levelList:
                if i >= len(item):
                    continue
                tempSet.add(item[i])
            tempDict[i] = list(tempSet)

        # 将每一级转成ztree的数据格式[{id:1, pId:0, name:it},....]
        retList = []
        nIndex = 1
        for key, val in tempDict.items():
            if 0 == key:
                retDict = {}
                retDict["id"] = nIndex
                retDict["pId"] = key
                retDict["name"] = val[key]
                retList.append(retDict)
                nIndex += 1
            else:
                for item in val:
                    retDict = {}
                    # 得到当前节点对应上级的id
                    for tList in levelList:
                        if item in tList:
                            nLen = len(tList)
                            parent = tList[nLen - 2]
                            for ret in retList:
                                if ret["name"] == parent:
                                    nFlag = ret["id"]

                    retDict["id"] = nIndex
                    retDict["pId"] = nFlag
                    retDict["name"] = item
                    retList.append(retDict)
                    nIndex += 1

        # 将ltree中的路径叶子节点名换成对应的中文名
        # 其实，也可以ltree的路径用中文表示，省着转换了
        # 这里，没有用中文路径的原因怕中文路径在字符串解析上出问题
        pathName = ""
        retName = ""
        for item in retList:
            tempName = item["name"]
            if tempName == "it":
                item["name"] = "IT"
                continue
            for tList in levelList:
                nLen = len(tList)
                if tempName in tList and \
                                tempName == tList[nLen - 1]:
                    pathName = ".".join(tList)
                    for soureDict in typeList:
                        for key, val in soureDict.items():
                            if key == pathName:
                                retName = val
                    break
            item["name"] = retName

        return retList

    def add_new_asset_info(self, data):
        asset_type = data['asset_type']
        from itdblib.common.type_info_utils import consumeList, phoneList
        data['store_state'] = '库存'
        if asset_type in consumeList():
            acs = AssetConsumeService()
            ret, msg = acs.store_new_consume_info(data)
        elif asset_type in phoneList():
            # 电话号码类存数
            ret, msg = AssetInfoService().validate_phone_is_single(data)
            if ret:
                acd = AssetInfoChNameToId()
                data = acd.get_asset_info_common_data(data)
                ret, msg = AssetPhoneInfoDal().store_new_phone_data(data)
                return ret, msg
        else:
            # 固定资产类存数
            data = self.transform_web_data(data)
            ret, msg = AssetInfoService().validate_add_new_asset_info(data)
            if ret:
                ret, msg = AssetInfoDal().add_new_asset_info(msg)
                return ret, msg
        return ret, msg

    def add_batch_asset_infos(self, asset_infos, operator):
        try:
            flag, actual_asset_infos, oper_asset_infos = self.get_actual_in_datas(asset_infos)
            if flag is False:
                return False, u'批量添加数据失败'
            ret, msg = self.add_actual_batch_datas(actual_asset_infos)
            # if ret:  # 如果批量入库成功，记录操作日志变更
            #     self.add_oper_batch_datas(oper_asset_infos, operator)
            return ret, msg
        except Exception, _ex:
            msg = "add_batch_asset_infos error: %s" % str(_ex)
            LOG.error(msg)
            return False, msg

    def transform_web_data(self, new_data):
        cds = ConstructDictService()
        new_data['type_info'] = cds.construct_type_info(new_data)
        return new_data

    def get_actual_in_datas(self, asset_infos):
        actual_asset_infos = []
        oper_asset_infos = []
        flag = True
        LOG.info('校验前端传过来的数据是否正确')
        for asset_info in asset_infos:
            oper_asset_infos.append(asset_info)
            LOG.info('校验' + asset_info['asset_id'])
            ret, msg = AssetInfoService(). \
                validate_add_new_asset_info(asset_info)
            actual_asset_infos.append(msg)
            if ret is False:
                flag = False
        LOG.info('校验前端传过来的数据结束')
        return flag, actual_asset_infos, oper_asset_infos

    def add_actual_batch_datas(self, actual_asset_infos):
        new_asset_infos = []
        cds = ConstructDictService()
        for asset_info in actual_asset_infos:
            # 上面数据全部校验，如果有一个值有错误，之前的全部都不入库
            # 这里为了批量入库需要转一下，和数据库字段一致
            asset_info['model_id'] = asset_info['model']
            asset_info['asset_type_id'] = asset_info['asset_type']
            asset_info['device_state_id'] = asset_info['device_state']
            asset_info['store_place_id'] = asset_info['store_place']
            asset_info['in_out_reason_id'] = asset_info['in_out_reason']
            asset_info['store_state_id'] = asset_info['store_state']
            asset_info['type_info'] = asset_info['type_info']
            asset_info['up_time'] = get_now_date()
            asset_info['update_time'] = get_now_date()
            new_asset_infos.append(asset_info)
        ret, msg = AssetInfoDal().add_batch_asset_infos(new_asset_infos)
        return ret, msg

    def add_oper_batch_datas(self, oper_asset_infos, operator):
        oper_infos = []
        for asset_info in oper_asset_infos:
            data = {}
            data['asset_id'] = asset_info['asset_id']
            data['oper_time'] = get_now_date()
            data['oper_type'] = '新增入库'
            data['operator'] = operator
            data['text'] = ''
            data['before_field'] = ''
            data['after_field'] = asset_info
            oper_infos.append(data)
        oid = OperationInfoDal()
        oid.add_batch_oper_infos(oper_infos)

    def muti_stock_in_different_assets(self, fileFullPath, operator, num):
        if num == 3:
            ret, msg = self.asset_stock_in_datas(fileFullPath, operator)
            if not ret:
                return ret, msg
            return self.phone_stock_in_datas(fileFullPath, operator)
        elif num == 1:
            return self.asset_stock_in_datas(fileFullPath, operator)
        elif num == 2:
            return self.phone_stock_in_datas(fileFullPath, operator)

    def add_batch_asset_phone_infos(self, asset_infos, operator):
        try:
            flag, actual_asset_infos = self.get_actual_phone_in_datas(asset_infos)
            if flag is False:
                return False, u'批量添加数据失败'
            import copy
            params = copy.deepcopy(actual_asset_infos)
            ret, msg = self.add_actual_batch_datas(actual_asset_infos)

            # if ret:  # 如果批量入库成功，记录操作日志变更
            #     self.add_oper_batch_datas(oper_asset_infos, operator)
            return ret, msg
        except Exception, _ex:
            msg = "add_batch_asset_infos error: %s" % str(_ex)
            LOG.error(msg)
            return False, msg

    def get_actual_phone_in_datas(self, asset_infos):
        actual_asset_infos = []
        aci = AssetInfoChNameToId()
        for asset_info in asset_infos:
            asset_info = aci.get_asset_info_common_data(asset_info)
            actual_asset_infos.append(asset_info)
        return self.add_actual_phone_batch_datas(actual_asset_infos)

    def add_actual_phone_batch_datas(self, actual_asset_infos):
        new_asset_infos = []
        cds = ConstructDictService()
        for asset_info in actual_asset_infos:
            # 上面数据全部校验，如果有一个值有错误，之前的全部都不入库
            # 这里为了批量入库需要转一下，和数据库字段一致
            asset_info['asset_type_id'] = asset_info['asset_type']
            asset_info['device_state_id'] = asset_info['device_state']
            asset_info['store_place_id'] = asset_info['store_place']
            asset_info['in_out_reason_id'] = asset_info['in_out_reason']
            asset_info['store_state_id'] = asset_info['store_state']
            asset_info['up_time'] = get_now_date()
            asset_info['update_time'] = get_now_date()
            asset_info['create_time'] = get_now_date()
            new_asset_infos.append(asset_info)
        ret, msg = AssetPhoneInfoDal().add_batch_asset_phone_infos(new_asset_infos)
        return ret, msg

    def asset_stock_in_datas(self, fileFullPath, operator):
        bFlag, dataSet = data_set_from_excel(fileFullPath)
        if not bFlag:
            return False, u'解析Excel失败'
        params = copy.deepcopy(dataSet)
        bRet, msg = self.add_batch_asset_infos(dataSet, operator)
        if bRet:
            aos = AssetOperateService()
            aos.construct_and_add_batch_operate_info(params, operator)
            LOG.info("[multi stock in] put data into database is success")
            return True, u'批量入库成功!'
        return False, u'批量入库失败'

    def phone_stock_in_datas(self, fileFullPath, operator):
        bFlag, dataSet = get_phone_data_set_from_excel(fileFullPath)
        if not bFlag:
            return False, u'解析Excel失败'
        params = copy.deepcopy(dataSet)
        bRet, msg = self.get_actual_phone_in_datas(dataSet)
        if bRet:
            aos = AssetOperateService()
            aos.construct_and_add_phone_batch_operate_info(params, operator)
            LOG.info("[multi stock in] put data into database is success")
            return True, u'批量入库成功!'
        return False, u'批量入库失败'