# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


import random
from oslo_db import options
from oslo_config import cfg
from testtools import TestCase
from tests.utils.app import QApplicationWsgiFixture
from itdblib.app import ItdbApplication
from qg.core import jsonutils

CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')


class TestAssertInfo(TestCase):

    def setUp(self):
        super(TestAssertInfo, self).setUp()
        self.wsgi_fixture = self.useFixture(
            QApplicationWsgiFixture(ItdbApplication))

    def test_add_new_asset_info_wrong_phone_number(self):
        """测试电话号码明显错误的话，是否保存成功
        """
        self.wsgi_fixture.login('zhen.pei')
        phone_num = "test-%d" % random.randint(10000000, 20000000)
        rlt = self.wsgi_fixture.wsgi.post("/stock_in/new/add", {
            "asset_type": "DID号",
            "phone_no": phone_num,
            "device_state": "可用",
            "store_place": "电子大厦",
            "in_out_reason": "一人多机归还",
            "user_name": "zhen.pei",
            "remark": "hello"
        })
        # print rlt.body
        self.assertEqual(rlt.status_code, 200)
        self.assertFalse(jsonutils.loads(rlt.body)["success"])
