# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from oslo.db import options
from oslo.config import cfg
from testtools import TestCase
from itdblib.db.api import get_engine
from itdblib.dal.asset_info_dal import AssetInfoDal
from itdblib.models.tb_asset_info import AssetInfoModel
import fixtures


CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')

from fixture import DataSet, SQLAlchemyFixture

class AssetInfoData(DataSet):
    class asset_info_data1:
        asset_id = 'QITNB007224'
        sn = '00005678'



class DBConnectionFx(fixtures.Fixture):

    def setUp(self):
        super(DBConnectionFx, self).setUp()
        CONF(['--config-file', 'tests/etc/unittest.ini'])

class DBFixture(fixtures.Fixture):

    def setUp(self):
        super(DBFixture, self).setUp()
        self.dbfixture = SQLAlchemyFixture(
            engine=get_engine(),
            env={'AssetInfoData': AssetInfoModel})
        self.data = self.dbfixture.data(AssetInfoData)
        self.data.setup()
        self.addCleanup(self.data.teardown)


class TestService(TestCase):

    def setUp(self):
        super(TestService, self).setUp()
        self.useFixture(DBConnectionFx())
        self.useFixture(DBFixture())

    def test_get_asset_info_all(self):
        assetInfos = AssetInfoDal().get_asset_info_all()
        self.assertEqual(1, len(assetInfos))

    def test_get_asset_info_num(self):
        num = AssetInfoDal().get_asset_info_num()
        self.assertEqual(1, num)

    def test_get_asset_info_by_id(self):
        assetInfo = AssetInfoDal().get_asset_info_by_id('QITNB007224')
        self.assertEqual(assetInfo.asset_id, 'QITNB007224')

    def test_get_asset_info_by_all_unique(self):
        assetInfo = AssetInfoDal().get_asset_info_by_all_unique('00005678')
        self.assertEqual(assetInfo.asset_id, 'QITNB007224')
    
    def test_get_asset_info_by_sn(self):
        assetInfo = AssetInfoDal().get_asset_info_by_sn('00005678')
        self.assertEqual(assetInfo.sn, '00005678')
        
    
