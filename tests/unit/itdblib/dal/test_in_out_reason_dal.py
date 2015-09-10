# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from fixture import DataSet, SQLAlchemyFixture
from oslo.db import options
from oslo.config import cfg
from testtools import TestCase
from itdblib.dal.in_out_reason_dal import InOutReasonDal
from itdblib.db.api import get_engine
from itdblib.models.dt_in_out_reason import InOutReason
import fixtures

CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')

from fixture import DataSet


class InOutData(DataSet):
    class in_or_out_sample1:
        id = 23
        in_or_out = 'IN_REASON'
        ch_name = u'借用归还'


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
            env={'InOutData': InOutReason})
        self.data = self.dbfixture.data(InOutData)
        self.data.setup()
        self.addCleanup(self.data.teardown)


class TestService(TestCase):

    def setUp(self):
        super(TestService, self).setUp()
        self.useFixture(DBConnectionFixture())
        self.useFixture(DBFixture())

    def test_get_out_reason_all(self):
        items = InOutReasonDal().get_in_reason_all()
        self.assertEqual(1, len(items))
        self.assertEqual(items[0].in_or_out, 'IN_REASON')

    def test_del_InOutReason_by_id(self):
        res = InOutReasonDal().get_reason_name_by_id(100)
        self.assertEqual(None, res)

        res_1 = InOutReasonDal().get_reason_name_by_id(23)
        self.assertEqual(res_1.in_or_out, 'IN_REASON')
