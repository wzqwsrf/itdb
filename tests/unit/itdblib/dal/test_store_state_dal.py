# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from fixture import SQLAlchemyFixture, DataSet
from oslo_db import options
from oslo_config import cfg
from testtools import TestCase
from qg.db import api as db_api

from itdblib.dal.store_state_dal import StoreStateDal
from itdblib.models.dt_store_state import StoreState
from itdblib.models.base import BASE
import fixtures

CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')

class StoreStateMock(DataSet):

    class storeState():
        ch_name = u'库存'



class DBConnectionFx(fixtures.Fixture):

    def setUp(self):
        super(DBConnectionFx, self).setUp()
        CONF(['--config-file', 'tests/etc/unittest.ini'])

class DBFixture(fixtures.Fixture):
    def setUp(self):
        super(DBFixture, self).setUp()
        self.engine = db_api.get_engine()
        self.engine.connect()
        self.dbfixture = SQLAlchemyFixture(
            engine=self.engine,
            env={
                "StoreStateMock": StoreState
            }
        )
        self.data = self.dbfixture.data(StoreStateMock)
        self.session = db_api.get_session()
        BASE.metadata.create_all(bind=self.engine)
        self.data.setup()
        self.addCleanup(self.data.teardown)

class TestStoreStateDal(TestCase):

    def setUp(self):
        super(TestStoreStateDal, self).setUp()
        self.useFixture(DBConnectionFx())
        self.dbfixture = self.useFixture(DBFixture())
        self.session = self.dbfixture.session
        self.dal = StoreStateDal()

    # unittest of method add_asset_type
    def test_add_asset_type(self):

        self.assertIsNone(self.dal.get_store_state_id_by_ch_name(ch_name=u'存在'))
        self.dal.add_asset_type(store_state=u'存在')
        self.assertEqual(u'存在', self.dal.get_store_state_id_by_ch_name(ch_name=u'存在').ch_name)
        self.dal.del_store_state_by_ch_name(store_state=u'存在')

    # unittest of method get_store_state(the store_state exist)
    def test_get_store_state(self):

        store_state = self.dal.get_store_state(store_state_id='1', store_state_name=u'库存')
        self.assertEqual(u'库存', store_state.ch_name)

    # unittest of method get_store_state(the store_state not exist)
    def test_get_store_state_not_exist(self):
        store_state = self.dal.get_store_state(store_state_id='1', store_state_name=u'库存库存')
        self.assertIsNone(store_state)

    # unittest of method del_store_state_by_ch_name(ch_name exist)
    #
    def test_del_store_state_by_ch_name(self):

        self.dal.add_asset_type(store_state=u'test')
        self.assertTrue(self.dal.del_store_state_by_ch_name(store_state=u'test'))

    # unittest of method del_store_state_by_ch_name(ch_name not exist)
    #
    def test_del_store_state_by_ch_name_not_exist(self):

        #self.dal.add_asset_type(store_state=u'test')
        self.assertTrue(self.dal.del_store_state_by_ch_name(store_state=u'test'))


