# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from sqlalchemy import and_
from qg.core import log as logging

from itdblib.dal.basedal import BaseDal
from itdblib.models.dt_asset_type import AssetTypeModel
from itdblib.models.mp_provider import Provider
from itdblib.models.mp_model import Model
from itdblib.models.dt_store_place import StorePlace
from itdblib.dal.store_place_dal import StorePlaceDal
from itdblib.dal.asset_type_dal import AssetTypeDal
from itdblib.dal.provider_dal import ProviderDal
from itdblib.dal.model_dal import ModelDal

LOG = logging.getLogger(__name__)


class AttributeManagerService(BaseDal):
    def __init__(self):
        self.session = self._getSession()

    def getAssetTypeById(self, assetId):
        """ 注： 根据id得到资产类型
        """
        q = self.session.query(AssetTypeModel) \
            .filter(AssetTypeModel.id == assetId) \
            .first()
        if q:
            return q.ch_name
        return None

    def getAssetTypeId(self, assetType):
        """ 根据资产类型得到id
        """
        q = self.session.query(AssetTypeModel) \
            .filter_by(ch_name=assetType) \
            .first()
        if q:
            return q.id
        else:
            return None

    def getAssetTypePath(self, assetType):
        """ 通过资产类型得到ltree路径
        """
        q = self.session.query(AssetTypeModel) \
            .filter_by(ch_name=assetType) \
            .first()
        return q.asset_path

    def getProviders(self, deviceType):
        """ 根据设备类型id得到所有品牌id
        """
        assetTypeId = self.getAssetTypeId(deviceType)
        if assetTypeId is None:
            LOG.error("[providers] asset type [%s] select error: "
                      % deviceType)
            return None

        providerList = self.session.query(Provider) \
            .filter_by(asset_type_id=assetTypeId) \
            .all()
        providers = set()
        for objProvider in providerList:
            providers.add(objProvider.id)
        return list(providers)

    def getProviderById(self, providerId):
        """ 注： 得到品牌名及设备类型id
        """
        q = self.session.query(Provider) \
            .filter(Provider.id == providerId) \
            .first()
        if q:
            return q.name, q.asset_type_id
        return None, None

    def getProviderId(self, assetTypeId, provider):
        """ 根据资产类型id及品牌得到品牌id
        """
        q = self.session.query(Provider) \
            .filter(and_(Provider.name == provider,
                         Provider.asset_type_id == assetTypeId)) \
            .first()
        if q:
            return q.id
        else:
            return None

    def getModels(self, assetType, provider):
        """ 根据品牌得到所有的该品牌的型号
        """
        assetTypeId = self.getAssetTypeId(assetType)
        if assetTypeId is None:
            LOG.error("[models] asset type [%s] select error: " % assetType)
            return None
        q = self.session.query(Provider) \
            .filter(and_(Provider.name == provider,
                         Provider.asset_type_id == assetTypeId)) \
            .first()
        providerId = q.id
        modelList = self.session.query(Model) \
            .filter_by(provider_id=providerId) \
            .all()

        models = []
        for objModel in modelList:
            models.append(objModel.name)
        return models

    def getModelId(self, providerId, model):
        """ 得到型号id
        """
        q = self.session.query(Model) \
            .filter(and_(Model.provider_id == providerId,
                         Model.name == model)) \
            .first()
        if q:
            return q.id
        else:
            return None

    def getModelById(self, modelId):
        """ 根据model的id得到型号、品牌id
        """
        q = self.session.query(Model) \
            .filter(Model.id == modelId) \
            .first()
        retDict = {}
        retDict["model"] = q.name
        retDict["providerId"] = q.provider_id
        return retDict

    def getHaveAssetTypeCount(self):
        """ 得到现有资产类别的数量
        """
        nCount = self.session.query(AssetTypeModel).count()
        return nCount

    def get_all_devices(self):
        """ 获取所有的设备类型、品牌、型号
        """
        retList = []

        objList = self.session.query(Model).all()
        for obj in objList:
            tempDict = {}
            tempDict["model"] = obj.name
            providerId = obj.provider_id
            provider, assetTypeId = self.getProviderById(providerId)
            if assetTypeId is None:
                continue
            assetType = self.getAssetTypeById(assetTypeId)
            if assetType is None:
                continue
            tempDict["provider"] = provider
            tempDict["asset_type"] = assetType
            retList.append(tempDict)
        return retList

    def addAssetClass(self, data):
        """ 添加资产类别
        """
        lPath = data.get("lpath")
        if not lPath:
            LOG.error("lpath value is empty!!!")
            return -1, u'添加失败'
        lpathList = lPath.split(".")
        nLen = len(lpathList)
        if 1 == nLen:
            # 说明添加资产类别
            assetClass = data.get("add_asset_class")
            assetClassEn = data.get("add_asset_class_en")
            return self.actual_add_asset_type(assetClass, assetClassEn,
                                                  lpathList, nLen)
        elif 2 == nLen:
             # 添加设备类型
             newAssetType = data.get("new_asset_type")
             newAssetTypeEn = data.get("new_asset_type_en")
             return self.actual_add_asset_type(newAssetType, newAssetTypeEn,
                                                  lpathList, nLen)
        else:
            try:
                # 添加品牌、型号
                checkList = []
                providerCh = data.get("add_provider")
                providerEn = data.get("add_provider_en")
                modelName = data.get("add_model")
                checkList.append(providerCh)
                checkList.append(providerEn)
                checkList.append(modelName)
                if not all(checkList):
                    LOG.error("add new provider model params are empty!!!")
                    return -1, u'填写内容为空，请检查'

                # 得到对应的资产类型id
                assetTypeName = lpathList[nLen - 1]
                atd = AssetTypeDal()
                assetTypeModel = atd.get_asset_type_id_by_ch_name(assetTypeName)
                assetTypeId = assetTypeModel.id if assetTypeModel else None

                # 添加品牌
                # 判断新添加的品牌是不是已有的品牌
                pd = ProviderDal()
                providerEn = providerEn.upper()
                providerModel = pd.get_prov_by_id_and_at(assetTypeId, providerEn)
                if providerModel:
                    # 现有的品牌，直接添加型号
                    LOG.info("add device provider is have device")
                    # 判断型号是否存在，如果存在，直接return重复，否则添加
                    provId = providerModel.id
                    md = ModelDal()
                    modelD = md.get_model_by_pd_ch(provId, modelName)
                    if modelD:
                        return -1, u'品牌：'+providerEn+'型号：'+modelName+'已经存在，请勿重复添加'
                    else:
                        md.add_model(provId, modelName)
                else:
                    # 新品牌
                    LOG.info("add device provider is new device")
                    pd.add_new_provider(assetTypeId, providerEn, providerCh)
                    md = ModelDal()
                    provModel = pd.get_prov_by_id_and_at(assetTypeId, providerEn)
                    md.add_model(provModel.id, modelName)
                return 0, u'添加成功'
            except Exception as _ex:
                LOG.error("error occured while add provider model: %s"
                          % str(_ex))
                return -1, u'添加失败'

    def removeAssetClassNode(self, dataNew):
        """ 删除树的节点(只删除设备类型)
            需要假删除（可以备份到两一个表里)
        """
        try:
            lpath = dataNew["lpath"]
            lpathList = lpath.split(".")
            nLen = len(lpathList)
            assetType = lpathList[nLen - 1]

            # 在删除之前得到该设备类型对应的品牌列表
            providerIdList = self.getProviders(assetType)

            # 删除该设备类型
            self.begin()
            itemAssetType = self.session.query(AssetTypeModel) \
                .filter_by(ch_name=assetType) \
                .first()
            self.session.delete(itemAssetType)
            self.commit()

            # 批量删除该品牌
            self.begin()
            self.session.query(Provider) \
                .filter(Provider.id.in_(tuple(providerIdList))) \
                .delete(synchronize_session=False)
            self.commit()

            # 遍历品牌列表删除对应的所有型号
            # 这种方式也是批量删除(最后一次提交)
            self.begin()
            for itemId in providerIdList:
                itemModel = self.session.query(Model) \
                    .filter_by(provider_id=itemId) \
                    .all()
                # 得到的itemModel是一个列表
                for mId in itemModel:
                    self.session.delete(mId)
            self.commit()
            return True
        except Exception as _ex:
            LOG.error("error occured while delete asset type: %s"
                      % str(_ex))
            return False

    def get_all_store_place_infos(self):
        """ 获取所有的库房信息
        """
        retList = []
        try:
            objList = self.session.query(StorePlace).all()
            for obj in objList:
                tempDict = {}
                tempDict["id"] = obj.id
                tempDict["storeplace"] = obj.ch_name
                tempDict["adminname"] = obj.admin_name
                retList.append(tempDict)
            return retList
        except Exception as _ex:
            LOG.error("get all storehouse msgs error: %s" % str(_ex))
            return retList

    def addStorePlace(self, data):
        # 添加库房信息,校验唯一性，如果已经存在，就不添加了。
        storeName = data["store_place"]
        adminName = data["admin_name"]
        try:
            spd = StorePlaceDal()
            storePlace = spd.get_store_place_id_by_ch_name(storeName)
            if storePlace:
                return False, u'库房地点' + storeName + u'已经存在，不能重复添加！'
            spd.add_store_place(storeName, adminName)
            return True, u'添加成功'
        except Exception as _ex:
            LOG.error("add new storehouse infos error: %s" % str(_ex))
            return False, u'添加失败'

    def actual_add_asset_type(self, assetClass, assetClassEn, lpathList, nLen):
        try:
            checkList = []
            checkList.append(assetClass)
            checkList.append(assetClassEn)
            if not all(checkList):
                LOG.error("add new asset class params are empty!!!")
                return -1, u'填写内容为空，请检查'
            # 得到ltree路径
            leafNode = lpathList[nLen - 1]
            assetPath = self.getAssetTypePath(leafNode)
            newPath = assetPath + "." + assetClassEn.lower()

            ast = AssetTypeDal()
            assetTypeModel = ast.get_asset_type_by_name_or_path(assetClass, newPath)
            if assetTypeModel:
                return -1, assetClass + '或者' + newPath + '已经存在，添加失败'
            ast.add_asset_type(assetClass, newPath)
            return 0, u'添加成功'
        except Exception as _ex:
            LOG.error("error occured while add asset class: %s" % str(_ex))
            return -1, u'添加失败'