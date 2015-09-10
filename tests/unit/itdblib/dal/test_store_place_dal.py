# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from oslo.db import options
from oslo.config import cfg
from testtools import TestCase
from itdblib.dal.store_place_dal import StorePlaceDal
import fixtures

CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')


class DBConnectionFx(fixtures.Fixture):

    def setUp(self):
        super(DBConnectionFx, self).setUp()
        CONF(['--config-file', 'tests/etc/unittest_jinlong.ini'])


class TestService(TestCase):

    def setUp(self):
        super(TestService, self).setUp()
        self.useFixture(DBConnectionFx())

    def test_get_store_place_all(self):
        allPlaces = StorePlaceDal().get_store_place_all()
        self.assertEqual(18, len(allPlaces))

    def test_get_store_place_id_by_ch_name(self):
        storeIdObj = StorePlaceDal().get_store_place_id_by_ch_name('维亚大厦')
        self.assertEqual(1,  storeIdObj.id)

    def test_get_store_place_name_by_id(self):
        storeNameObj = StorePlaceDal().get_store_place_name_by_id(1)
        self.assertEqual(storeNameObj.ch_name, u'维亚大厦')

    # new add 
    # pragma mark - 这有个bug，没有提交事务,也就是没有self.begin()
    """
    def add_store_place(self, ch_name):
        storePlace = StorePlace()
        storePlace.ch_name = ch_name
        self.session.add(storePlace)
        self.commit()

    """
    def test_add_store_place(self):
        StorePlaceDal().add_store_place(u'金龙大厦')

    # new del
    def test_del_store_place(self):
        StorePlaceDal().del_store_place_by_ch_name(u'电子大厦')

