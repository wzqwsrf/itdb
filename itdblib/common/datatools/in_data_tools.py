# -*- coding: utf-8 -*-
#
# author: wangzq <wangzhenqing1008@163.com>
#
from qg.core import log as logging
from openpyxl import load_workbook
from itdblib.common.asset_info_utils import AssetInfoUtils
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
LOG = logging.getLogger(__name__)


def format_field_map():
    aiu = AssetInfoUtils()
    chlist = aiu.input_excel_ch_list()
    enlist = aiu.input_excel_en_list()
    e_len = len(enlist)
    return dict([(chlist[i], enlist[i]) for i in range(e_len)])


def get_data_from_excel(fileFullPath, sheetName='assets'):
    """ read and set data from excel
    """
    fieldMap = format_field_map()
    dataSet = []
    try:
        wb = load_workbook(filename=fileFullPath)
        print('Available sheets are %s' % ','.join(wb.get_sheet_names()))
        sheet = wb[sheetName]
        head = map(lambda x: x.value, sheet.rows[0])
        for row in sheet.rows[1:]:
            data_row = {}
            for i, cell in enumerate(row):
                if head[i] == 'IMEI':
                    data_row['imei'] = ''
                if head[i] == u'版本号':
                    data_row['version'] = ''
                if cell.value:
                    if fieldMap[head[i]] == 'asset_id':
                        data_row[fieldMap[head[i]]] = str(cell.value).strip().upper()
                    else:
                        data_row[fieldMap[head[i]]] = str(cell.value).strip()
                else:
                    data_row[fieldMap[head[i]]] = ''
            data_row['store_state'] = '库存'
            dataSet.append(data_row)
        return dataSet
    except Exception, _ex:
        print("error occured while read data from excel : %s" % str(_ex))
        return dataSet


def get_all_datas(pathname):
    dataSet = get_data_from_excel(pathname)
    dlen = len(dataSet)
    asset_list = []
    asset_dict = {}
    for i in range(dlen):
        asset_list.append(str(dataSet[i]['asset_id']).upper())
        asset_dict[dataSet[i]['asset_id'].upper()] = dataSet[i]['user_name']
    return (asset_list, asset_dict)

if __name__ == '__main__':
    get_data_from_excel('/home/zhenqingwang/Desktop/123.xlsx')
