# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from oslo.db import options
from oslo.config import cfg
from testtools import TestCase
from itdblib.dal.asset_type_dal import AssetTypeDal
import fixtures

CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')


class DBConnectionFx(fixtures.Fixture):

    def setUp(self):
        super(DBConnectionFx, self).setUp()
        CONF(['--config-file', 'tests/etc/unittest.ini'])


class TestService(TestCase):

    def setUp(self):
        super(TestService, self).setUp()
        self.useFixture(DBConnectionFx())

    def test_1_add_asset_type(self):
        asset_type = AssetTypeDal().search_by_path('*.test.test.jyn')
        self.assertEqual(0, len(asset_type))

        AssetTypeDal().add_asset_type('test_jyn', 'test.test.test.jyn')

    def test_2_get_asset_type_by_ch_name(self):
        asset_type = AssetTypeDal().search_by_path('*.test.test.jyn')
        self.assertEqual(1, len(asset_type))

        asset_type = AssetTypeDal().get_asset_type_id_by_ch_name('test_jyn')
        self.assertEqual('test.test.test.jyn', asset_type.asset_path)

    def test_3_delete_asset_type_by_ch_name(self):
        asset_type = AssetTypeDal().search_by_path('*.test.test.jyn')
        self.assertEqual(1, len(asset_type))

        res = AssetTypeDal().del_asset_type_by_ch_name('test_jyn')
        self.assertEqual(True, res)

    def test_4_get_asset_type_by_path(self):
        asset_type = AssetTypeDal().search_by_path('*.test.test.jyn')
        self.assertEqual(0, len(asset_type))

