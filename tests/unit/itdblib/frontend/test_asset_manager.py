# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from oslo_db import options
from oslo_config import cfg
from testtools import TestCase
from tests.utils.app import QApplicationWsgiFixture
from itdblib.app import ItdbApplication
from qg.core import jsonutils

CONF = cfg.CONF
CONF.register_opts(options.database_opts, 'database')


class TestLogin(TestCase):

    def setUp(self):
        super(TestLogin, self).setUp()
        self.wsgi_fixture = self.useFixture(
            QApplicationWsgiFixture(ItdbApplication))

    def test_login(self):
        """测试登录
        """
        r = self.wsgi_fixture.wsgi.get("/asset_manager/asset_manager")
        self.assertEqual(r.status_code, 302)

    def test_search_asset_right(self):
        """测试搜索资产信息(正确输入)
        """
        self.wsgi_fixture.login('jingyao.shi')
        r = self.wsgi_fixture.wsgi.post("/asset_manager/asset/jingyao.shi", {
            'iDisplayStart': 0,
            'iDisplayLength': 30
        })
        rjson = jsonutils.loads(r.body)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(rjson["count"], 1)

    def test_search_asset_wrong(self):
        """测试搜索资产信息(错误输入)
        """
        self.wsgi_fixture.login('jingyao.shi')
        r = self.wsgi_fixture.wsgi.post("/asset_manager/asset/'", {
            'iDisplayStart': 0,
            'iDisplayLength': 30
        })
        rjson = jsonutils.loads(r.body)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(rjson["count"], 0)
