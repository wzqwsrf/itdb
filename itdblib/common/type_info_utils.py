# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

def type_info_en_list():
    return ['imei', 'version', 'mac', 'userful_life']


def type_info_ch_list():
    return ['IMEI', '版本信息', 'MAC地址', '有效期限']


def wireList():
    return ['phone', 'pad']


def macList():
    return ['笔记本', '台式机']


def vpnList():
    return ['VPN令牌']


def consumeList():
    return consumePeopleList() + consumeAssetList()


def consumePeopleList():
    return ['键盘',
            '鼠标',
            '扇热架',
            '小型交换机',
            'IP话机',
            'USB移动硬盘',
            'U盘	',
            '普通无线路由器'
    ]


def consumeAssetList():
    return ['笔记本内存',
            '台式机内存',
            'SATA硬盘',
            'SSD硬盘',
            '笔记本电池',
            '笔记本电源适配器',
            'ATA话机盒'
    ]


def phoneList():
    return ['分机号', 'DID号']


def type_info_en_dict():
    type_dict = {}
    en_list = type_info_en_list()
    ch_list = type_info_ch_list()
    d_len = len(en_list)
    for i in range(d_len):
        type_dict[en_list[i]] = ch_list[i]
    return type_dict


def type_info_ch_dict():
    type_dict = {}
    en_list = type_info_en_list()
    ch_list = type_info_ch_list()
    d_len = len(en_list)
    for i in range(d_len):
        type_dict[ch_list[i]] = en_list[i]
    return type_dict


#无线资产(phone\pad)不同部分
def assetInfoWireEnlist():
    return ['imei', 'version']


#固定资产(笔记本、台式机)不同部分
def assetInfoMacEnlist():
    return ['mac']


#配件资产（VPN令牌）不同部分
def assetInfoVpnEnlist():
    return ['userful_life']