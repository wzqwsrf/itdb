# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from fixture import DataSet, SQLAlchemyFixture
from oslo.db import options
from oslo.config import cfg
from testtools import TestCase
from itdblib.dal.provider_dal import ProviderDal
from itdblib.db.api import get_engine
from itdblib.models.mp_provider import Provider
import fixtures

CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')

from fixture import DataSet


class MpProviderData(DataSet):
    class it_wireless:
        id = 5
        name = u"DELL"
        ch_name = u"戴尔"
        asset_type_id = "32"


class DBConnectionFixture(fixtures.Fixture):

    def setUp(self):
        super(DBConnectionFixture, self).setUp()
        CONF(['--config-file', 'tests/etc/unittest.ini'])


class DBFixture(fixtures.Fixture):

    def setUp(self):
        super(DBFixture, self).setUp()
        self.dbfixture = SQLAlchemyFixture(
            engine=get_engine(),
            env={'MpProviderData': Provider})
        self.data = self.dbfixture.data(MpProviderData)
        self.data.setup()
        self.addCleanup(self.data.teardown)


class TestService(TestCase):

    def setUp(self):
        super(TestService, self).setUp()
        self.useFixture(DBConnectionFixture())
        self.useFixture(DBFixture())

    def test_1_provider_dal(self):
        items = ProviderDal().get_provider_all()
        self.assertEqual(1, len(items))

    def test_2_get_prov_name_by_atd_md(self):
        items = ProviderDal().get_prov_name_by_atd_md(32, 5)
        self.assertEqual(u'DELL', items.name)

        items_1 = ProviderDal().get_prov_name_by_atd_md(32, 6)
        self.assertEqual(None, items_1)

        items_1 = ProviderDal().get_prov_name_by_atd_md('a>', 6)
        self.assertEqual(None, items_1)

    def test_3_del_provider_by_id(self):
        res = ProviderDal().del_provider_by_id(100)
        self.assertEqual(None, res)

        res_1 = ProviderDal().del_provider_by_id(5)
        self.assertEqual(True, res_1)
