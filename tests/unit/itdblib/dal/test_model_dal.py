# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


import fixtures
from fixture import SQLAlchemyFixture, DataSet
from oslo.config import cfg
from oslo.db import options
from qg.db import api as db_api
from testtools import TestCase

from itdblib.dal.model_dal import ModelDal
from itdblib.models.base import BASE
from itdblib.models.mp_model import Model


CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')


class ModelDS(DataSet):
    # noinspection PyClassHasNoInit
    class Model1:
        id = 1
        provider_id = 11
        name = "model1"

    # noinspection PyClassHasNoInit
    class Model2:
        id = 2
        provider_id = 22
        name = "model2"

    class Model22:
        id = 3
        provider_id = 22
        name = "model22"


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
                "ModelDS": Model
            }
        )
        self.data = self.dbfixture.data(ModelDS)
        self.session = db_api.get_session()
        BASE.metadata.create_all(bind=self.engine)
        self.data.setup()
        self.addCleanup(self.data.teardown)


class ModelDALTestCase(TestCase):
    def setUp(self):
        super(ModelDALTestCase, self).setUp()
        self.useFixture(DBConnectionFixture())
        self.dbfixture = self.useFixture(DBFixture())
        self.session = self.dbfixture.session
        self.dal = ModelDal()

    def tearDown(self):
        super(ModelDALTestCase, self).tearDown()
        self.session.execute('delete from mp_model')

    def test_get_model_all(self):
        ret = self.dal.get_model_all()
        self.assertEqual(len(ret), 3)

    def test_get_model_by_prov_id(self):
        # 通过id返回的还是一个集合，会有1对多吗
        model = self.dal.get_model_by_prov_id(11)
        self.assertEqual(model[0].name, 'model1')

    def test_add_model(self):
        self.dal.add_model(3, 'model3')
        ret = self.dal.get_model_all()
        self.assertEqual(len(ret), 4)

    def test_del_model_by_id(self):
        # 这个测试跑不过去
        self.dal.del_model_by_id(1)
        ret = self.dal.get_model_all()
        self.assertEqual(2, len(ret))

    def test_get_model_by_pd_ch(self):
        model = self.dal.get_model_by_pd_ch(11, 'model1')
        self.assertIsNotNone(model)
        self.assertEqual(model.name, 'model1')
        self.assertEqual(model.provider_id, 11)

        model = self.dal.get_model_by_pd_ch(1, 'model2')
        self.assertIsNone(model)

    def test_get_model_name_by_id(self):
        model = self.dal.get_model_name_by_id(1)
        self.assertIsNotNone(model)
        self.assertEqual(model.name, 'model1')

    def test_get_model_list_by_prov_id(self):
        models = self.dal.get_model_list_by_prov_id(22)
        self.assertIsNotNone(models)
        self.assertEqual(len(models), 2)
