# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

from itdblib.common.hr_intf import fetch_info_by_id


# 根据rtx_id获取leader
def get_employee_owner(rtx_id):
    res_dict = fetch_info_by_id('userId=', rtx_id)
    if judge_value_is_none(res_dict):
        return u'员工不存在'
    data = res_dict['data']
    if data['hire_type'] == u'正式':
        return rtx_id
    return data['manager_email'].split('@')[0]


def get_rtx_id_by_sn(sn):
    res_dict = fetch_info_by_id('sn=', sn)
    if judge_value_is_none(res_dict):
        return sn
    data = res_dict['data']
    return data['user_name']


def judge_value_is_none(res_dict):
    if len(res_dict) == 0:
        return True
    data = res_dict['data']
    if len(data) == 0:
        return True
    return False


# 将输入的员工编号转为rtx_id
def get_actual_rtx_id(id):
    if id == '' or id is None:
        return ''
    if id[0:2] == 'Q0':
        return get_rtx_id_by_sn(id)
    return id