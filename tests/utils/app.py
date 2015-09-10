# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


import fixture
import mock
from webtest import TestApp
import fixtures


class QApplicationWsgiFixture(fixtures.Fixture):

    def __init__(self, app_klass, app_args=None, app_kwargs=None,
                 *args, **kwargs):
        super(QApplicationWsgiFixture, self).__init__(*args, **kwargs)
        self.app_klass = app_klass
        self.app_args = [] if app_args is None else app_args
        self.app_kwargs = {} if app_kwargs is None else app_kwargs
        self.session = {}

    @mock.patch('sys.argv', ['test-app', '--config-file', 'etc/test/itdb.conf'])
    def setUp(self):
        super(QApplicationWsgiFixture, self).setUp()
        app = self.app_klass(*self.app_args, **self.app_kwargs)
        app._step_invoke("configure")
        app._step_invoke("run", do_pre=True, do_fn=False, do_post=False)
        self.app = app
        self.wsgi = TestApp(app.wsgi_app)
        patcher = mock.patch('itdblib.app.session', self.session)
        patcher.start()

    def login(self, rtx_id):
        self.session["rtx_id"] = rtx_id
