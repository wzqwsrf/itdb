# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from datetime import timedelta

from flask import (
    session,
    request,
    url_for,
    redirect
)
from oslo_config import cfg
import oslo_db.options
from qg.web.app import QFlaskApplication
from qg.core.app.exts.log import QLogExtension


web_opts = [
    cfg.StrOpt('title',
               default='itdb',
               help='the web titile'),
    cfg.StrOpt('base_url',
               default='',
               help='the web base url')
]

server_opts = [
    cfg.IntOpt('max_content_length',
               default=5 * 1024 * 1024,
               help='the upload file size limit (bytes)'),
    cfg.IntOpt('session_lefttime',
               default=2,
               help='the session lefttime (hours)')
]

CONF = cfg.CONF
CONF.register_opts(web_opts, 'WWW')
CONF.register_opts(server_opts, 'SERVER')
oslo_db.options.set_defaults(CONF)


class ItdbApplication(QFlaskApplication):
    name = "itdb"
    version = "0.1"

    def create(self):
        super(ItdbApplication, self).create()
        self.register_extension(QLogExtension())

    def init_app(self):
        super(ItdbApplication, self).init_app()
        app = self.flask_app

        app.secret_key = 'kuaishiyongshuangjiegunhenghenghaxi'
        app.permanent_session_lefttime = timedelta(hours=2)
        app.template_folder = "itdblib/frontend/templates"
        app.static_folder = "itdblib/frontend/static"

        # @app.before_request
        # def before_request():
        #     if ('rtx_id' not in session) and \
        #                     request.blueprint in (
        #                     'stock_in',
        #                     'stock_out',
        #                     'asset_manager',
        #                     'asset_phone',
        #                     'asset_consume',
        #                     'attribute_manager'):
        #         return redirect(url_for('index.login', ret=request.url))

        @app.context_processor
        def default_context_processor():
            result = {}
            result['title'] = CONF.WWW.title.decode('UTF-8')
            result['base_url'] = CONF.WWW.base_url
            result['static_url'] = CONF.WWW.base_url + "/static"
            result['current_user'] = session.get('rtx_id')
            return result

        # init route
        import itdblib.frontend.views.index as index

        app.register_blueprint(index.bp, url_prefix='')

        import itdblib.frontend.views.stock_in as stock_in

        self.register_blueprint(stock_in.bp, url_prefix='/stock_in')

        import itdblib.frontend.views.stock_out as stock_out

        self.register_blueprint(stock_out.bp, url_prefix='/stock_out')

        import itdblib.frontend.views.asset_manager as asset_manager

        self.register_blueprint(asset_manager.bp, url_prefix='/asset_manager')

        import itdblib.frontend.views.attribute_manager as attribute_manager

        self.register_blueprint(attribute_manager.bp,
                                url_prefix='/attribute_manager')

        import itdblib.frontend.views.asset_info as asset_info

        self.register_blueprint(asset_info.bp, url_prefix='/asset_info')

        import itdblib.frontend.views.asset_consume as asset_consume

        self.register_blueprint(asset_consume.bp, url_prefix='/asset_consume')

        import itdblib.frontend.views.asset_phone as asset_phone

        self.register_blueprint(asset_phone.bp, url_prefix='/asset_phone')

        import itdblib.frontend.views.asset_info_api as asset_info_api

        self.register_blueprint(asset_info_api.bp, url_prefix='/asset')
