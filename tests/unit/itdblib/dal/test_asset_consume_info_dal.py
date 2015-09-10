# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from fixture import DataSet, SQLAlchemyFixture
from oslo_db import options
from oslo_config import cfg
from testtools import TestCase
import fixtures

from itdblib.db.api import get_engine
from itdblib.models.base import BASE
from itdblib.models.tb_asset_consume_info import AssetConsumeInfoModel
from itdblib.dal.asset_consume_info_dal import AssetConsumeInfoDal

CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')

class AssetConsumeInfoData(DataSet):
    class example1:
        asset_type_id = 1
        store_place_id = 2
        store_state_id = 3
        device_state_id = 4
        in_out_reason_id = 5
        model_id = 6
        in_num = 7
        out_num = 8
        user_name = 'shadow.zhang'


class DBConnectionFixture(fixtures.Fixture):

    def setUp(self):
        super(DBConnectionFixture, self).setUp()
        CONF(['--config-file', 'tests/etc/unittest.ini'])


class DBFixture(fixtures.Fixture):

    def setUp(self):
        super(DBFixture, self).setUp()
        self.dbfixture = SQLAlchemyFixture(
            engine=get_engine(),
            env={'AssetConsumeInfoData': AssetConsumeInfoModel})
        self.data = self.dbfixture.data(AssetConsumeInfoData)
        BASE.metadata.create_all(get_engine())
        self.data.setup()
        self.addCleanup(self.data.teardown)


class TestDeviceStateDal(TestCase):

    def setUp(self):
        super(TestDeviceStateDal, self).setUp()
        self.useFixture(DBConnectionFixture())
        self.useFixture(DBFixture())

    def test_get_all_asset_consume(self):
        dal = AssetConsumeInfoDal()
        records = dal.get_asset_consume_info_all()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].user_name, 'shadow.zhang')
