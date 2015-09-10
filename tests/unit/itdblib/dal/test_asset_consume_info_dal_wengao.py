# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from fixture import SQLAlchemyFixture, DataSet
from oslo.db import options
from oslo.config import cfg
from testtools import TestCase
from qg.db import api as db_api

from itdblib.dal.asset_consume_info_dal import AssetConsumeInfoDal
from itdblib.models.tb_asset_consume_info import AssetConsumeInfoModel
from itdblib.models.base import BASE
import fixtures


CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')


class AssetConsumeInfoMock(DataSet):

    class AssetConsumeInfoModel():
        id=1
        asset_type_id = 1
        model_id = 1
        user_name = "abc"
        store_place_id = 1
        store_state_id = 1
        device_state_id = 1
        in_num = 0
        out_num = 0
        in_out_reason_id = 0
        remark = 'remark'


class StorePlaceMock(DataSet):
    class StorePlace():
        id = 1
        ch_name = 'store_place1'


class ModelMock(DataSet):
    class Model():
        id = 1
        provider_id = 1
        name = 'model1'

class AssetTypeMock(DataSet):
    class AssetTypeModel():
        id = 1
        ch_name = 'asset_path1'
        asset_path = 'asset_path1'

class StoreStateMock(DataSet):
    class StoreState():
        id = 1
        ch_name = 'state1'


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
                "AssetConsumeInfoMock": AssetConsumeInfoModel
            }
        )
        self.data = self.dbfixture.data(AssetConsumeInfoMock)
        self.session = db_api.get_session()
        BASE.metadata.create_all(bind=self.engine)
        self.data.setup()
        self.addCleanup(self.data.teardown)

class TestAssetConsumeInfoDal(TestCase):

    def setUp(self):
        super(TestAssetConsumeInfoDal, self).setUp()
        self.useFixture(DBConnectionFx())
        self.dbfixture = self.useFixture(DBFixture())
        self.session = self.dbfixture.session


    def test_store_new_consume_data(self):

        data = {
            'asset_type': 1,  #id, not name
            'model': 1,       #id, not name
            'store_place': 1, #id, not name
            'in_num': 3,
            'remark': 'test',
            'user_name': 'ops'
        }
        AssetConsumeInfoDal().store_new_consume_data(data)
        model = AssetConsumeInfoDal().get_actual_asset_by_type_model_place(
            asset_type=1,
            model_id=1,
            store_place_id=1,
            store_state=1
        )
        self.assertEqual('test', model.remark)
        self.assertEqual('ops', model.user_name)
