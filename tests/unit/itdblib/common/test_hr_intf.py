# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


from testtools import TestCase
from itdblib.common import hr_intf


class TestService(TestCase):

    def test_call_http_intf(self):
        # itdblib/common/corehr_api_utils.get_employee_owner
        param = "userId="
        _id = "ning.xie"
        hr_one_intf = "http://qunar.it/api/employees/?require=info"
        ret_dict = hr_intf.call_http_intf("%s%s" % (hr_one_intf, param+_id))
        self.assertFalse(ret_dict["data"])
        
