# -*- coding: utf-8 -*-
#
# author: wangzq <wangzhenqing1008@163.com>
#

import json
from datetime import date, datetime
import decimal
from flask import Response


def _jsonfy(mix):
    result = None
    if isinstance(mix, list):
        result = []
        for i in mix:
            result.append(_jsonfy(i))
    elif isinstance(mix, dict):
        result = {}
        for k, v in mix.items():
            k = _jsonfy(k)
            v = _jsonfy(v)
            result[k] = v
    elif isinstance(mix, datetime):
        result = mix.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(mix, date):
        result = mix.strftime('%Y-%m-%d')
    elif isinstance(mix, decimal.Decimal):
        result = float(mix)
    else:
        return mix
    return result


def jsondump(mix):
    mix = _jsonfy(mix)
    return json.dumps(mix)


def ajax_success(msg=u'success', data=u'', **kwargs):
    result = {}
    result.update(kwargs)
    result["success"] = True
    result["msg"] = msg
    result["data"] = data
    return jsondump(result)


def ajax_error(msg, **kwargs):
    result = {}
    result.update(kwargs)
    result["success"] = False
    result["msg"] = msg
    return jsondump(result)


def api_success(msg=u'success', data=u'', **kwargs):
    return Response(ajax_success(msg, data, **kwargs), status=200,
                    mimetype='application/json')


def api_error(msg, **kwargs):
    return Response(ajax_error(msg, **kwargs), status=200,
                    mimetype='application/json')
