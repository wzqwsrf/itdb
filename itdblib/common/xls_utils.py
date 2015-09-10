# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import xlwt
import tempfile
import datetime


def writeExcel(list, savefile=None, chlist=[], enlist=[]):
    if savefile is None:
        savefile = tempfile.mkstemp()[1]
    style_date = xlwt.XFStyle()
    style_date.num_format_str = 'yyyy-mm-dd hh:mm:ss'
    wb = xlwt.Workbook()
    ws = wb.add_sheet('sheet1')
    for i in range(len(chlist)):
        ws.write(0, i, chlist[i])
    row = 1
    for i in range(len(list)):
        for j in range(len(enlist)):
            if type(list[i][enlist[j]]) in (datetime.date, datetime.datetime):
                ws.write(row, j, list[i][enlist[j]], style_date)
            else:
                ws.write(row, j, list[i][enlist[j]])
        row += 1
    wb.save(savefile)
    return savefile
