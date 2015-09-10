# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from oslo_db import options
from oslo_config import cfg
from testtools import TestCase
from itdblib.dal.asset_phone_info_dal import AssetPhoneInfoDal
import fixtures
from itdblib.db.api import get_session
from itdblib.models.tb_asset_phone_info import AssetPhoneInfoModel

CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')


class DBConnectionFx(fixtures.Fixture):

    def setUp(self):
        super(DBConnectionFx, self).setUp()
        CONF(['--config-file', 'tests/etc/unittest.ini'])


'''
class DeviceStateDS(DataSet):
    # noinspection PyClassHasNoInit
    class DeviceState1:
        remark = ""
        # 'remark':'@#$%^&', 'user_name':'huangchenghong', 'asset_type':0, 'store_place':1,
        #        'device_state':12, 'store_state':123, 'in_out_reason':'2123123', 'phone_no':'073188888888/8532'
'''


class TestAssetPhoneInfoDal(TestCase):

    def setUp(self):
        super(TestAssetPhoneInfoDal, self).setUp()
        self.useFixture(DBConnectionFx())

    def test_1_new_phone_type(self):
        data = {'remark':'@#$%^&', 'user_name':'huangchenghong', 'asset_type':0, 'store_place':1,
                'device_state':12, 'store_state':123, 'in_out_reason':'2123123', 'phone_no':'073188888888/8532'}
        flag, asset_new_phone =  AssetPhoneInfoDal().store_new_phone_data(data)
        self.assertEqual(True, flag)

    def test_2_get_advanced_phone_search_val_count(self):
        params = {'store_state':'123', 'device_state':12, 'store_place':1, 'in_out_reason':'2123123',
                  'asset_type':0, 'model_list':'who is model_list', 'date_from1':'2014-11-20',
                  'date_to1':'2014-11-22', 'date_from2':'2014-11-20', 'date_to2':'2014-11-22'}
        model = AssetPhoneInfoDal().get_advanced_phone_search_val_count(params)
        self.assertEqual(1, int(model))

    def test_3_delete(self):
        session = get_session()
        session.begin(subtransactions=True)
        #params = {'store_state':'123', 'device_state':12, 'store_place':1, 'in_out_reason':'2123123',
        #          'asset_type':0, 'model_list':'who is model_list', 'date_from1':'2014-11-20',
        #          'date_to1':'2014-11-22', 'date_from2':'2014-11-20', 'date_to2':'2014-11-22'}
        models = session.query(AssetPhoneInfoModel).filter(AssetPhoneInfoModel.in_out_reason_id=='2123123').all()
        #print len(models)
        for model in models:
            session.delete(model)
        session.commit()
