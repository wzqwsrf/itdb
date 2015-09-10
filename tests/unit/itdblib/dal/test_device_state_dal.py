# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from fixture import DataSet, SQLAlchemyFixture
from oslo.db import options
from oslo.config import cfg
from testtools import TestCase
import fixtures

from itdblib.db.api import get_engine
from itdblib.models.base import BASE
from itdblib.models.dt_device_state import DeviceState
from itdblib.dal.device_state_dal import DeviceStateDal

CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')


class DeviceStateData(DataSet):
    class example1:
        ch_name = u"可用"

    class example2:
        ch_name = u"不可用"

    class example3:
        ch_name = u"报废中"

    class example4:
        ch_name = u"报废无"


class DBConnectionFixture(fixtures.Fixture):

    def setUp(self):
        super(DBConnectionFixture, self).setUp()
        CONF(['--config-file', 'tests/etc/unittest.ini'])


class DBFixture(fixtures.Fixture):

    def setUp(self):
        super(DBFixture, self).setUp()
        self.dbfixture = SQLAlchemyFixture(
            engine=get_engine(),
            env={'DeviceStateData': DeviceState})
        self.data = self.dbfixture.data(DeviceStateData)
        BASE.metadata.create_all(get_engine())
        self.data.setup()
        self.addCleanup(self.data.teardown)


class TestDeviceStateDal(TestCase):

    def setUp(self):
        super(TestDeviceStateDal, self).setUp()
        self.useFixture(DBConnectionFixture())
        self.useFixture(DBFixture())

    def test_get_all_device_state(self):
        dal = DeviceStateDal()
        records = dal.get_all_device_state()
        device_state_list = []
        for record in records:
            device_state_list.append(record.ch_name)
        self.assertEqual(len(records), 4)
        self.assertEqual(u'可用' in device_state_list, True)
        self.assertEqual(u'不可用' in device_state_list, True)
        self.assertEqual(u'报废中' in device_state_list, True)
        self.assertEqual(u'报废无' in device_state_list, True)

    def test_add_device_state(self):
        dal = DeviceStateDal()
        new_type = u'啦啦啦'
        dal.add_device_state(new_type)
        self.assertEqual(len(dal.get_all_device_state()), 5)
        dal.del_device_state(new_type)
