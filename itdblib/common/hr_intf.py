# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>


import json
import urllib2

from oslo_config import cfg
from qg.core import log as logging

LOG = logging.getLogger(__name__)

interface_opt = [
    cfg.StrOpt('hr_one_intf',
               default='',
               help='fetch one'),

    cfg.StrOpt('hr_all_intf',
               default='',
               help='fetch all'),

    cfg.StrOpt('hr_auto_intf',
               default='',
               help='hr_auto_intf')
]

CONF = cfg.CONF
CONF.register_opts(interface_opt, 'INTERFACE')

__all = (
    'fetchOne',
    'fetchAll'
)


def fetch_info_by_id(param, id):
    return fetch_info(param + id)


def auto_show_employee_info(id):
    """ get all employee infos
    """
    retDict = {}
    url = CONF.INTERFACE.hr_auto_intf + id
    retDict = call_http_intf(url)
    return retDict


def fetch_info(param):
    """ @param: rtx_id
    """
    retDict = {}
    try:
        LOG.info("current rtx_id is : %s" % param)
        url = CONF.INTERFACE.hr_one_intf
        url = "%s%s" % (url, param)
    except Exception as _ex:
        LOG.error("error occured while format url: %s" % str(_ex))
        return retDict

    retDict = call_http_intf(url)
    return retDict


def fetch_all_infos():
    """ get all employee infos
    """
    retDict = {}
    url = CONF.INTERFACE.hr_all_intf
    retDict = call_http_intf(url)
    return retDict


def call_http_intf(url):
    """ method: GET
    """
    retDict = {}
    try:
        request = urllib2.Request(url)
        retVal = urllib2.urlopen(request, timeout=20)
    except urllib2.HTTPError as _ex:
        LOG.error("The server couldn't fullfill the request")
        LOG.error("Error code : %s" % str(_ex))
        return retDict
    except urllib2.URLError as _ex:
        LOG.error("fetch the url content is error")
        LOG.error("Error code : %s" % str(_ex))
        return retDict
    except Exception as _ex:
        LOG.error("error occured while fetch one info: %s" % str(_ex))
        return retDict
    else:
        res = retVal.read()
        retDict = json.loads(res)
        return retDict
