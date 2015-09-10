# -*- coding: utf-8 -*-
#
# author: wangzq <wangzhenqing1008@163.com>
#

class AssetInfoUtils():
    def __init__(self):
        pass

    @staticmethod
    def get_asset_info_ch_list():
        ch_list = [u'资产编号', u'设备类别', u'品牌', u'型号',
                   u'S/N', u'MAC地址', u'设备状态', u'使用人', u'责任人',
                   u'存放地点', u'资产状态', u'出入库原因', u'详细信息',
                   u'IMEI', u'版本信息', u'有效期限',
                   u'启用时间', u'创建时间', u'更新时间', u'备注信息']
        return ch_list

    @staticmethod
    def get_asset_info_en_list():
        en_list = ['asset_id', 'asset_type', 'provider', 'model',
                   'sn', 'mac', 'device_state', 'user_name', 'owner',
                   'store_place', 'store_state', 'in_out_reason', 'type_info',
                   'imei', 'version', 'userful_life',
                   'up_time', 'create_time', 'update_time', 'remark']
        return en_list

    @staticmethod
    def add_asset_info_en_list():
        en_list = ['asset_id', 'asset_type', 'provider', 'model',
                   'device_state', 'user_name', 'store_place',
                   'store_state', 'in_out_reason']
        return en_list

    @staticmethod
    def input_excel_ch_list():
        ch_list = [
            u'资产编号',
            u'资产类别',
            u'品牌',
            u'型号',
            u'SN',
            u'MAC',
            U'IMEI',
            u'版本信息',
            u'到期时间',
            u'设备状态',
            u'入库原因',
            u'资产状态',
            u'存放地点',
            u'库房管理员',
            u'备注信息'
        ]
        return ch_list

    @staticmethod
    def input_excel_en_list():
        en_list = [
            'asset_id',
            'asset_type',
            'provider',
            'model',
            'sn',
            'mac',
            'imei',
            'version',
            'userful_life',
            'device_state',
            'in_out_reason',
            'store_state',
            'store_place',
            'user_name',
            'remark'
        ]
        return en_list

    @staticmethod
    def input_phone_excel_ch_list():
        ch_list = [u'电话号码', u'号码类别', u'号码状态', u'库房管理员',
                   u'存放地点', u'资产状态', u'入库原因',
                   u'备注信息']
        return ch_list

    @staticmethod
    def input_phone_excel_en_list():
        en_list = ['phone_no', 'asset_type', 'device_state', 'user_name',
                   'store_place', 'store_state', 'in_out_reason',
                   'remark']
        return en_list

    @staticmethod
    def output_excel_ch_list():
        ch_list = [
            u'资产编号',
            u'资产类别',
            u'品牌',
            u'型号',
            u'SN',
            u'设备状态',
            u'入库原因',
            u'资产状态',
            u'存放地点',
            u'库房管理员',
            u'详细信息',
            u'备注信息',
            u'启用时间',
            u'创建时间',
            u'更新时间'
        ]
        return ch_list

    @staticmethod
    def output_excel_en_list():
        en_list = [
            'asset_id',
            'asset_type',
            'provider',
            'model',
            'sn',
            'device_state',
            'in_out_reason',
            'store_state',
            'store_place',
            'user_name',
            'type_info',
            'remark',
            'up_time',
            'create_time',
            'update_time'
        ]
        return en_list

    @staticmethod
    def get_advanced_list():
        re_list = ["store_state", "store_place", "device_state",
                   "in_reason", "out_reason", "asset_type", "provider",
                   "model", "date_from1", "date_to1",
                   "date_from2", "date_to2", "oper_name"]
        return re_list

    @staticmethod
    def get_new_asset_common_info():
        en_list = ['asset_type', 'device_state',
                   'store_place', 'store_state', 'in_out_reason']
        return en_list

    @staticmethod
    def add_asset_phone_info_en_list():
        en_list = ['asset_id', 'asset_type', 'provider', 'model',
                   'device_state', 'user_name', 'store_place',
                   'store_state', 'in_out_reason']
        return en_list

    @staticmethod
    def get_phone_ch_list():
        ch_list = [u'电话号码', u'号码类别', u'号码状态', u'使用人', u'责任人',
                   u'存放地点', u'资产状态', u'出入库原因',
                   u'启用时间', u'创建时间', u'更新时间', u'备注信息']
        return ch_list

    @staticmethod
    def get_phone_en_list():
        en_list = ['phone_no', 'asset_type', 'device_state', 'user_name', 'owner',
                   'store_place', 'store_state', 'in_out_reason',
                   'up_time', 'create_time', 'update_time', 'remark']
        return en_list

    @staticmethod
    def get_consume_ch_list():
        ch_list = [
            u'ID',
            u'资产类别',
            u'品牌',
            u'型号',
            u'设备状态',
            u'出入库原因',
            u'已有数量',
            u'新增数量',
            u'资产状态',
            u'存放地点',
            u'库房管理员',
            u'备注信息',
        ]
        return ch_list

    @staticmethod
    def get_consume_en_list():
        en_list = [
            'id',
            'asset_type',
            'provider',
            'model',
            'device_state',
            'in_out_reason',
            'in_num1',
            'in_num2',
            'store_state',
            'store_place',
            'user_name',
            'remark',
        ]
        return en_list

    @staticmethod
    def get_oper_phone_enlist():
        en_list = ['phone_no', 'asset_type',
                   'device_state', 'user_name', 'store_place',
                   'store_state', 'in_out_reason', 'remark']
        return en_list

    @staticmethod
    def output_consume_excel_ch_list():
        ch_list = [
            u'资产类别',
            u'品牌',
            u'型号',
            u'设备状态',
            u'出入库原因',
            u'库存数量',
            u'发出数量',
            u'剩余数量',
            u'资产状态',
            u'存放地点',
            u'库房管理员',
            u'备注信息',
            u'启用时间',
            u'创建时间',
            u'更新时间'
        ]
        return ch_list

    @staticmethod
    def output_consume_excel_en_list():
        en_list = [
            'asset_type',
            'provider',
            'model',
            'device_state',
            'in_out_reason',
            'consume_all',
            'out_num',
            'in_num',
            'store_state',
            'store_place',
            'user_name',
            'remark',
            'up_time',
            'create_time',
            'update_time'
        ]
        return en_list

    @staticmethod
    def output_phone_excel_ch_list():
        ch_list = [u'电话号码', u'号码类别', u'号码状态', u'使用人',
                   u'存放地点', u'资产状态', u'出入库原因',
                   u'启用时间', u'创建时间', u'更新时间', u'备注信息']
        return ch_list

    @staticmethod
    def output_phone_excel_en_list():
        en_list = ['phone_no', 'asset_type', 'device_state', 'user_name',
                   'store_place', 'store_state', 'in_out_reason',
                   'up_time', 'create_time', 'update_time', 'remark']
        return en_list
