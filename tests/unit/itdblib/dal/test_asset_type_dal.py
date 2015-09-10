# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from fixture import DataSet, SQLAlchemyFixture
from oslo.db import options
from oslo.config import cfg
from testtools import TestCase
from itdblib.dal.asset_type_dal import AssetTypeDal
from itdblib.db.api import get_engine
from itdblib.models.dt_asset_type import AssetTypeModel
import fixtures

CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')

from fixture import DataSet


class AssetTypeData(DataSet):
    class it_wireless:
        ch_name = u"无线资产"
        asset_path = "it.wireless"


class DBConnectionFixture(fixtures.Fixture):

    def setUp(self):
        super(DBConnectionFixture, self).setUp()
        CONF(['--config-file', 'tests/etc/unittest.ini'])


class DBFixture(fixtures.Fixture):

    def setUp(self):
        super(DBFixture, self).setUp()
        print get_engine()
        self.dbfixture = SQLAlchemyFixture(
            engine=get_engine(),
            env={'AssetTypeData': AssetTypeModel})
        self.data = self.dbfixture.data(AssetTypeData)
        self.data.setup()
        self.addCleanup(self.data.teardown)


class TestService(TestCase):

    def setUp(self):
        super(TestService, self).setUp()
        self.useFixture(DBConnectionFixture())
        self.useFixture(DBFixture())

    def test_get_asset_type_all(self):
        items = AssetTypeDal().get_asset_type_all()
        self.assertEqual(1, len(items))
