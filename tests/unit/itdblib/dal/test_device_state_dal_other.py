# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


import fixtures
from fixture import SQLAlchemyFixture, DataSet
from itdblib.dal.device_state_dal import DeviceStateDal
from itdblib.models.base import BASE
from itdblib.models.dt_device_state import DeviceState
from oslo_db import options
from oslo_config import cfg
from qg.db import api as db_api
from testtools import TestCase

CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')


class DeviceStateDS(DataSet):
    # noinspection PyClassHasNoInit
    class DeviceState1:
        ch_name = "ch_name_1"

    # noinspection PyClassHasNoInit
    class DeviceState2:
        ch_name = "ch_name_2"


class DBConnectionFixture(fixtures.Fixture):
    def setUp(self):
        super(DBConnectionFixture, self).setUp()
        CONF(['--config-file', 'tests/etc/unittest.ini'])


# noinspection PyAttributeOutsideInit
class DBFixture(fixtures.Fixture):
    def setUp(self):
        super(DBFixture, self).setUp()
        self.engine = db_api.get_engine()
        self.engine.connect()
        self.dbfixture = SQLAlchemyFixture(
            engine=self.engine,
            env={
                "DeviceStateDS": DeviceState
            }
        )
        self.data = self.dbfixture.data(DeviceStateDS)
        self.session = db_api.get_session()
        BASE.metadata.create_all(bind=self.engine)
        self.data.setup()
        self.addCleanup(self.data.teardown)


class DeviceStateDALTestCase(TestCase):
    def setUp(self):
        super(DeviceStateDALTestCase, self).setUp()
        self.useFixture(DBConnectionFixture())
        self.dbfixture = self.useFixture(DBFixture())
        self.session = self.dbfixture.session
        self.dal = DeviceStateDal()

    def tearDown(self):
        super(DeviceStateDALTestCase, self).tearDown()
        self.session.execute('delete from dt_device_state')

    def test_get_all_device_state(self):
        ret = self.dal.get_all_device_state()
        self.assertEqual(len(ret), 2)

    def test_add_device_state(self):
        ret = self.dal.add_device_state('abc')
        self.assertEqual(ret, True)
        self.assertEqual(len(self.dal.get_all_device_state()), 3)

    def test_del_device_state(self):
        ret = self.dal.add_device_state('abc')
        self.assertEqual(ret, True)
        self.assertEqual(len(self.dal.get_all_device_state()), 3)
        ret = self.dal.del_device_state('abc')
        self.assertTrue(ret)

    def test_update_device_state(self):
        ret = self.dal.add_device_state('abc')
        self.assertEqual(ret, True)
        self.assertEqual(len(self.dal.get_all_device_state()), 3)
        ret = self.dal.del_device_state('abc1')
        self.assertTrue(ret)

    def test_get_device_state_id_by_ch_name(self):
        ret = self.dal.get_device_state_id_by_ch_name('ch_name_1')
        self.assertEqual(ret.ch_name, 'ch_name_1')

    def test_get_device_state_name_by_id(self):
        ret = self.dal.get_device_state_id_by_ch_name('ch_name_2')
        id = ret.id
        device_state = self.dal.get_device_state_name_by_id(id)
        self.assertEqual(device_state.ch_name, 'ch_name_2')
