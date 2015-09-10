# -*- coding: utf-8 -*-
#
# author: wangzq <wangzhenqing1008@163.com>
#

import sys

from itdblib.common.datatools.in_data_tools import get_all_datas
from itdblib.common.datatools.tb_asset_info import (
    get_need_data,
    get_exist_sn_list)
from itdblib.common.datatools.in_data_tools import (
    get_data_from_excel
)

import xlwt
import tempfile

def get_all_in_data():
    pathname = '/home/zhenqingwang/Desktop/123.xlsx'
    asset_list, asset_dict = get_all_datas(pathname)
    table_datas = get_need_data(asset_list)
    user_name_equal = []
    user_name_not_equal = []
    for table_data in table_datas:
        asset_id = table_data.asset_id.upper()
        user_name = asset_dict[asset_id]
        # print asset_id
        # print table_data.user_name
        # print user_name
        if table_data.user_name.upper().strip() != user_name.upper():
            user_name_not_equal.append(table_data.asset_id)
        else:
            user_name_equal.append(asset_id)
    print u'名字相等记录数', len(user_name_equal)
    print u'名字不相等记录数', len(user_name_not_equal)
    params = get_data_from_excel(pathname)
    list3 = get_exist_sn_list(params, user_name_equal, user_name_not_equal)
    print u'sn相等记录数', len(list3)
    print list3
    write_excel(params, '/home/zhenqingwang/Desktop/zhenqing.xlsx', user_name_equal, user_name_not_equal, list3)


def write_excel(list, savefile, list1, list2, list3):
    chlist = [u'资产编号',
              u'设备类型',
              u'品牌',
              u'型号',
              u'mac',
              u'sn',
              u'设备状态',
              u'存储地点',
              u'入库原因',
              u'使用人',
              u'IMEI',
              u'版本号',
              u'备注'
    ]
    enlist = ['asset_id',
              'asset_type',
              'provider',
              'model',
              'mac',
              'sn',
              'device_state',
              'store_place',
              'in_out_reason',
              'user_name',
              'imei',
              'version',
              'remark'
    ]
    if savefile is None:
        savefile = tempfile.mkstemp()[1]
    style1 = xlwt.XFStyle()
    pattern1 = xlwt.Pattern()  # Create the Pattern
    pattern1.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern1.pattern_fore_colour = 2
    style1.pattern = pattern1  # Add Pattern to Style
    style2 = xlwt.XFStyle()
    pattern2 = xlwt.Pattern()
    pattern2.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern2.pattern_fore_colour = 3
    style2.pattern = pattern2  # Add Pattern to Style
    style3 = xlwt.XFStyle()
    pattern3 = xlwt.Pattern()
    pattern3.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern3.pattern_fore_colour = 4
    style3.pattern = pattern3  # Add Pattern to Style
    wb = xlwt.Workbook()
    ws = wb.add_sheet('assets')
    for i in range(len(chlist)):
        ws.write(0, i, chlist[i])
    row = 1
    for i in range(len(list)):
        if list[i]['asset_id'].upper() in list1:
            for j in range(len(enlist)):
                value = unicode(list[i][enlist[j]], 'utf8')
                ws.write(row, j, value, style2)
        elif list[i]['asset_id'].upper() in list2:
            for j in range(len(enlist)):
                value = unicode(list[i][enlist[j]], 'utf8')
                ws.write(row, j, value, style1)
        else:
            if list[i]['sn'] == '4T6QCV1':
                print list[i]['asset_id']
                print list[i]['sn'] in list3
            if list[i]['sn'].upper() in list3:
                for j in range(len(enlist)):
                    value = unicode(list[i][enlist[j]], 'utf8')
                    ws.write(row, j, value, style3)
            else:
                for j in range(len(enlist)):
                    value = unicode(list[i][enlist[j]], 'utf8')
                    ws.write(row, j, value)
        row += 1
    wb.save(savefile)
    return savefile


if __name__ == '__main__':
    get_all_in_data()