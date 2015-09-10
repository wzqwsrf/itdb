/**
 * Created by zhenqing.wang on 7/24/14.
 */

function getAssetInfoAssetTypeChlist() {
    var chlist = ['设备类别'];
    return chlist;
}

function getAssetInfoAssetTypeEnlist() {
    var enlist = ['asset_type'];
    return enlist;
}

//获取入库信息展示的基础内容
function getAssetInfoNewChlist() {
    var chlist = ['资产编号', '品牌', '型号',
        'S/N', '设备状态', '存放地点', '库房管理员',
        '入库原因'];
    return chlist;
}

//获取入库信息展示的基础内容
function getAssetInfoNewEnlist() {

    var enlist = ['asset_id', 'provider', 'model',
        'sn', 'device_state', 'store_place', 'user_name',
        'in_out_reason'];
    return enlist;
}

//获取编辑页面的中文字段
function getAssetInfoEditChlist() {
    var chlist = ['资产编号', '设备类别', '品牌', '型号',
        'S/N', '设备状态', '办公地点', '使用人',
        '资产状态', '出库原因'];
    return chlist;
}

//获取编辑页面的英文字段
function getAssetInfoEditEnlist() {

    var enlist = ['asset_id', 'asset_type', 'provider', 'model',
        'sn', 'device_state', 'store_place', 'user_name',
        'store_state', 'in_out_reason'];
    return enlist;
}

function getAssetInfoOldChlist() {
    var chlist = ['资产编号', '设备类别', '品牌', '型号',
        'S/N', '设备状态', '办公地点', '使用人', '责任人',
        '资产状态', '出库原因'];
    return chlist;
}

//获取table tb_asset_info表的英文字段
function getAssetInfoOldEnlist() {

    var enlist = ['asset_id', 'asset_type', 'provider', 'model',
        'sn', 'device_state', 'store_place', 'user_name', 'owner',
        'store_state', 'in_out_reason'];
    return enlist;
}

//获取table tb_asset_info表的中文字段
function getNewAssetInfoChlist() {
    var chlist = ['资产编号', '设备类别', '品牌', '型号',
        'S/N', 'MAC地址', '设备状态', '存放地点', '使用人',
        '资产状态', '出入库原因', '详细信息', '备注信息', '启用时间'];
    return chlist;
}

//获取table tb_asset_info表的英文字段
function getNewAssetInfoEnlist() {

    var enlist = ['asset_id', 'asset_type', 'provider', 'model',
        'sn', 'mac', 'device_state', 'store_place', 'user_name',
        'store_state', 'in_out_reason', 'type_info', 'remark', 'up_time'];
    return enlist;
}

//展示已有资产入库内容中文字段
function getAssetInfoInChRight() {
    var chlist = ['设备状态', '入库原因', '存放地点',
        '库房管理员', '备注信息'];
    return chlist;
}

//展示已有资产入库内容英文字段
function getAssetInfoInEnRight() {

    var enlist = ['device_state', 'in_out_reason', 'store_place',
        'user_name', 'remark'];
    return enlist;
}

//展示已有资产出库内容中文字段
function getAssetInfoOutChRight() {
    var chlist = ['设备状态', '出库原因', '办公地点',
        '使用人', '备注信息'];
    return chlist;
}

//展示已有资产出库内容英文字段
function getAssetInfoOutEnRight() {

    var enlist = ['device_state', 'in_out_reason', 'store_place',
        'user_name', 'remark'];
    return enlist;
}

function getAssetManagerEnList() {
    var enlist = ['asset_id', 'asset_type', 'provider', 'model',
        'sn', 'mac', 'device_state', 'in_out_reason', 'user_name',
        'store_place', 'store_state', 'imei', 'version', 'remark'];
    return enlist;
}

function getAssetConsumeInEnlist() {
    var enlist = ['asset_type', 'provider',
        'model', 'store_place', 'consume_num1',
        'consume_num2', 'user_name', 'remark'];
    return enlist;
}

function getAssetConsumeInChlist() {
    var chlist = ['耗材类别', '品牌', '型号',
        '存放地点', '已有数量', '耗材数量', '使用人', '备注信息'];
    return chlist;
}

function getAssetConsumeOutEnlist() {
    var enlist = ['asset_type', 'provider',
        'model', 'store_place', 'consume_num1',
        'store_state', 'store_place2',
        'consume_num2', 'user_name', 'remark'];
    return enlist;
}

function getAssetConsumeOutChlist() {
    var chlist = ['耗材类别', '品牌', '型号',
        '出库地点', '库存数量', '资产状态', '入库地点',
        '耗材数量', '使用人', '备注信息'];
    return chlist;
}

function wireList() {
    return ['phone', 'pad'];
}

function macList() {
    return ['笔记本', '台式机'];
}

function vpnList() {
    return ['VPN令牌'];
}

function consumeList() {
    var list1 = consumePeopleList();
    var list2 = consumeAssetList();
    var list = list1.concat(list2);
    return list;
}

function consumePeopleList() {
    return ['键盘',
        '鼠标',
        '扇热架',
        '小型交换机',
        'IP话机',
        'USB移动硬盘',
        'U盘	',
        '普通无线路由器'
    ]
}

function consumeAssetList() {
    return ['笔记本内存',
        '台式机内存',
        'SATA硬盘',
        'SSD硬盘',
        '笔记本电池',
        '笔记本电源适配器',
        'ATA话机盒'
    ]
}

function phoneList() {
    return ['分机号', 'DID号'];
}

//无线资产(phone\pad)不同部分
function getAssetInfoWireChlist() {
    var chlist = ['IMEI', '版本信息'];
    return chlist;
}

//无线资产(phone\pad)不同部分
function getAssetInfoWireEnlist() {
    var enlist = ['imei', 'version'];
    return enlist;
}

//固定资产(笔记本、台式机)不同部分
function getAssetInfoMacChlist() {
    var chlist = ['MAC地址'];
    return chlist;
}

//固定资产(笔记本、台式机)不同部分
function getAssetInfoMacEnlist() {
    var enlist = ['mac'];
    return enlist;
}

//配件资产（VPN令牌）不同部分
function getAssetInfoVpnChlist() {
    var chlist = ['有效期限'];
    return chlist;
}

//配件资产（VPN令牌）不同部分
function getAssetInfoVpnEnlist() {
    var enlist = ['userful_life'];
    return enlist;
}

function type_info_en_list() {
    return ['imei', 'version', 'mac', 'userful_life'];
}

function type_info_ch_list() {
    return ['IMEI', '版本信息', 'MAC地址', '有效期限'];
}

function consume_info_en_list() {
    var enlist = ['provider', 'model',
        'device_state', 'store_place', 'in_out_reason',
        'in_num1', 'in_num2', 'user_name'];
    return enlist;
}

function consume_info_ch_list() {

    var chlist = ['品牌', '型号',
        '设备状态', '存放地点', '入库原因',
        '已有数量', '入库数量', '库房管理员'];
    return chlist;
}

function phone_info_en_list() {
    var enlist = ['phone_no', 'device_state',
        'store_place', 'in_out_reason',
        'user_name'];
    return enlist;
}

function phone_info_ch_list() {

    var chlist = ['电话号码', '号码状态',
        '存放地点', '入库原因', '库房管理员'];
    return chlist;
}


function getPhoneRightEnList() {
    var enlist = ['p_device_state',
        'p_store_place', 'p_in_out_reason',
        'p_user_name', 'p_remark'];
    return enlist;
}

function getPhoneRightChList() {
    var chlist = ['号码状态',
        '存放地点', '入库原因',
        '库房管理员', '备注信息'];
    return chlist;
}

function getPhoneInfoOldEnlist() {

    var enlist = ['phone_no', 'asset_type',
        'device_state', 'store_place',
        'user_name', 'remark',
        'store_state', 'in_out_reason'];
    return enlist;
}

function getConsumeRightEnList() {
    var enlist = ['c_device_state',
        'c_store_place', 'c_in_out_reason',
        'c_in_num',
        'c_user_name', 'c_remark'];
    return enlist;
}

function getConsumeRightChList() {
    var chlist = ['设备状态',
        '存放地点', '入库原因',
        '入库数量',
        '库房管理员', '备注信息'];
    return chlist;
}

function getConsumeInfoOldEnlist() {

    var enlist = ['asset_type', 'provider',
        'model', 'device_state', 'store_place',
        'user_name', 'remark', 'in_num',
        'store_state', 'in_out_reason'];
    return enlist;
}

function getPhoneOutRightEnList() {
    var enlist = [
        'p_store_place',
        'p_in_out_reason',
        'p_remark'];
    return enlist;
}

function getPhoneOutRightChList() {
    var chlist = [
        '办公地点',
        '出库原因',
        '备注信息'];
    return chlist;
}

//获取table tb_asset_info表的英文字段
function getDetailConsumeInEnlist() {

    var enlist = ['asset_type', 'provider', 'model',
        'device_state', 'store_state', 'in_out_reason',
        'consume_all', 'out_num', 'in_num',
        'store_place', 'user_name', 'remark',
        'up_time', 'create_time',
        'update_time'];
    return enlist;
}

//获取table tb_asset_info表的中文字段
function getDetailConsumeInChlist() {
    var chlist = ['耗材类别', '品牌', '型号',
        '设备状态', '资产状态', '入库原因',
        '库存总量', '发出数量', '剩余数量',
        '存放地点', '库房管理员', '备注信息',
        '启用时间', '创建时间',
        '更新时间'];
    return chlist;
}

//获取table tb_asset_info表的英文字段
function getDetailConsumeOutEnlist() {

    var enlist = ['asset_type', 'provider', 'model',
        'device_state', 'store_state', 'in_out_reason',
        'in_num', 'store_place', 'user_name', 'remark',
        'up_time', 'create_time',
        'update_time'];
    return enlist;
}

//获取table tb_asset_info表的中文字段
function getDetailConsumeOutChlist() {
    var chlist = ['耗材类别', '品牌', '型号',
        '设备状态', '资产状态', '出库原因',
        '使用数量', '办公地点', '使用人', '备注信息',
        '启用时间', '创建时间',
        '更新时间'];
    return chlist;
}

function getConsumeOutPeopleRightEnList() {
    var enlist = [
        'c_in_out_reason', 'c_store_place',
        'c_out_num', 'c_user_name',
        'c_remark'];
    return enlist;
}

function getConsumeOutPeopleRightChList() {
    var chlist = [
        '出库原因', '办公地点',
        '出库数量', '使用人',
        '备注信息'];
    return chlist;
}

function getConsumeOutAssetRightEnList() {
    var enlist = [
        'c_in_out_reason', 'c_store_place',
        'c_out_num', 'asset_id',
        'c_remark'];
    return enlist;
}

function getConsumeOutAssetRightChList() {
    var chlist = [
        '出库原因', '办公地点',
        '出库数量', '需升级资产编号',
        '备注信息'];
    return chlist;
}

