# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from datetime import datetime
from fixture import DataSet, SQLAlchemyFixture
from oslo_db import options
from oslo_config import cfg
from testtools import TestCase
from itdblib.dal.asset_consume_info_dal import AssetConsumeInfoDal
from itdblib.db.api import get_engine
from itdblib.models.tb_asset_consume_info import AssetConsumeInfoModel
import fixtures

CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')


DT_FORMAT = '%Y-%m-%d %H:%M:%S'
str2dt = lambda s: datetime.strptime(s, DT_FORMAT)


class AssetConsumeInfos(DataSet):
    class asset_consume_info_1:
        id = 1
        asset_type_id = 1
        model_id = 1
        user_name = 'songkuan'
        store_place_id = 1
        store_state_id = 1
        device_state_id = 1
        in_num = 1
        out_num = 1
        in_out_reason_id = 1
        up_time = str2dt('2014-11-21 20:00:00')
        create_time = str2dt('2014-11-20 20:00:00')
        update_time = str2dt('2014-11-21 22:00:00')
        remark = 'test first'


class DBConnectionFixture(fixtures.Fixture):

    def setUp(self):
        super(DBConnectionFixture, self).setUp()
        CONF(['--config-file', 'tests/etc/unittest.ini'])


class DBFixture(fixtures.Fixture):

    def setUp(self):
        super(DBFixture, self).setUp()
        self.dbfixture = SQLAlchemyFixture(
            engine=get_engine(),
            env={'AssetConsumeInfos': AssetConsumeInfoModel})
        self.data = self.dbfixture.data(AssetConsumeInfos)

        self.data.setup()
        self.addCleanup(self.data.teardown)


class TestService(TestCase):

    def setUp(self):
        super(TestService, self).setUp()
        self.useFixture(DBConnectionFixture())
        self.useFixture(DBFixture())

    def test_get_actual_asset_by_type_model_place(self):
        hit = AssetConsumeInfoDal().get_actual_asset_by_type_model_place(
            1, 1, 1, 1)
        self.assertIsNotNone(hit)
        self.assertIsInstance(hit, AssetConsumeInfoModel)
        self.assertEqual(hit.create_time, str2dt('2014-11-20 20:00:00'))

    def test_get_asset_consume_info_by_search_val_one_wildcard(self):
        hit = AssetConsumeInfoDal()\
            .get_asset_consume_info_by_search_val_one('%')

        # 程序bug: 未对搜索字符串中%转义，测试失败
        # 已对%转义
        self.assertIsNone(hit)

    def test_get_asset_consume_info_by_search_val_one_empty(self):
        hit = AssetConsumeInfoDal()\
            .get_asset_consume_info_by_search_val_one('')

        # 程序bug: 搜索字符串未空时仍然有搜索结果，测试失败
        # 前端限制,这个字段一定不为空
        self.assertIsNone(hit)
