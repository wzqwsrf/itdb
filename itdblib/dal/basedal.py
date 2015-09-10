# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from itdblib.db.api import get_session


class BaseDal(object):
    def __init__(self):
        super(BaseDal, self).__init__()
        self.session = self._getSession()

    def _getSession(self):
        return get_session()

    def begin(self, subtransactions=False):
        self.session.begin(subtransactions=subtransactions)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()
