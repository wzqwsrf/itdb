/**
 * Created by zhenqingwang on 7/24/14.
 */

function getSelectValue(id, url, value) {
    //  下拉框值从数据库选择,并且设置默认值
    $.ajax({
        "dataType": 'json',
        "type": "GET",
        "url": url,
        "success": function (resp) {
            $("#" + id).find("option").remove();
            var opstr = $.parseStr('<option value="%s" selected="selected">%s</option>', value, value);
            $("#" + id).append(opstr);
            var r_len = resp.length;
            for (var i = 0; i < r_len; i++) {
                opstr = $.parseStr('<option value="%s">%s</option>', resp[i].ch_name, resp[i].ch_name);
                $("#" + id).append(opstr);
            }
        }
    });
}

function postSelectValue(id, url, asset_value, value) {
    //  下拉框值从数据库选择,并且设置默认值
    $.ajax({
        "dataType": 'json',
        "type": "POST",
        "url": url,
        'data': {return_val: asset_value},
        "success": function (resp) {
            $("#" + id).find("option").remove();
            var opstr = $.parseStr('<option value="%s" selected="selected">%s</option>', value, value);
            $("#" + id).append(opstr);
            var r_len = resp.length;
            for (var i = 0; i < r_len; i++) {
                opstr = $.parseStr('<option value="%s">%s</option>', resp[i], resp[i]);
                $("#" + id).append(opstr);
            }
        },
        error: function (resp) {
            console.log(resp);
        }
    });
}

function postDefaultSelectValue(id, url, asset_value, value) {
    //  下拉框值从数据库选择,并且设置默认值
    $.ajax({
        "dataType": 'json',
        "type": "POST",
        "url": url,
        'data': {return_val: asset_value},
        "success": function (resp) {
            $("#" + id).find("option").remove();
            var r_len = resp.length;
            for (var i = 0; i < r_len; i++) {
                var opstr = $.parseStr('<option value="%s">%s</option>', resp[i], resp[i]);
                if (resp[i] == value) {
                    opstr = $.parseStr('<option value="%s" selected="selected">%s</option>', value, value);
                }
                $("#" + id).append(opstr);
            }
        },
        error: function (resp) {
            console.log(resp);
        }
    });
}

function getDefaultSelectValue(id, url, value) {
    //  下拉框值从数据库选择,并且设置默认值
    $.ajax({
        "dataType": 'json',
        "type": "GET",
        "url": url,
        "success": function (resp) {
            $("#" + id).find("option").remove();
            var r_len = resp.length;
            for (var i = 0; i < r_len; i++) {
                var opstr = $.parseStr('<option value="%s">%s</option>', resp[i].ch_name, resp[i].ch_name);
                if (resp[i].ch_name == value) {
                    opstr = $.parseStr('<option value="%s" selected="selected">%s</option>', resp[i].ch_name, resp[i].ch_name);
                }
                $("#" + id).append(opstr);
            }
        }
    });
}

/*   判断输入框值是否为空*/
function isNull(value) {
    if (value == undefined || value == '' || value == null) {
        return true;
    }
    return false;
}

function getOwnerByRtxId(id, value) {
    $.ajax({
        "dataType": 'json',
        "type": "POST",
        "url": '/asset_info/owner',
        'data': {return_val: value},
        "success": function (resp) {
            $("#" + id).val(resp.owner);
        }
    });
}

function saveOperInfo(params) {
    $.ajax({
        url: "/asset_info/save_oper",
        type: "POST",
        data: params,
        success: function (resp) {
            showSuccessTips(resp);
        },
        error: function (resp) {
            showErrorTips();
        }
    });
}


function getSelectInValue(id, url, value) {
    //  下拉框值从数据库选择,并且设置默认值
    $.ajax({
        "dataType": 'json',
        "type": "GET",
        "url": url,
        "success": function (resp) {
            $("#" + id).find("option").remove();
            var opstr = $.parseStr('<option value="%s" selected="selected">%s</option>', value, value);
            $("#" + id).append(opstr);
            var r_len = resp.length;
            for (var i = 0; i < r_len; i++) {
                if (resp[i].ch_name == '采购入库'
                    || resp[i].ch_name == '报废中'
                    || resp[i].ch_name == '报废无') {
                    continue;
                }
                opstr = $.parseStr('<option value="%s">%s</option>', resp[i].ch_name, resp[i].ch_name);
                $("#" + id).append(opstr);
            }
        }
    });
}

function mergeList(list1, list2){
    var len = list2.length;
    for(var i = 0; i < len; i++){
        list1.push(list2[i]);
    }
    return list1;
}


function getEnChList(value) {
    var chlist = [];
    var enlist = [];
    if (containsValue(wireList(), value)) {
        chlist = getAssetInfoWireChlist();
        enlist = getAssetInfoWireEnlist();
    } else if (containsValue(macList(), value)) {
        chlist = getAssetInfoMacChlist();
        enlist = getAssetInfoMacEnlist();
    } else if (containsValue(vpnList(), value)) {
        chlist = getAssetInfoVpnChlist();
        enlist = getAssetInfoVpnEnlist();
    }
    return [enlist, chlist]
}

function transformDivName(chname, store_state) {
    if (store_state == '库存') {
        if (chname == '出库原因') {
            chname = '入库原因';
        }
        if (chname == '使用人') {
            chname = '库存管理员';
        }
        if (chname == '办公地点') {
            chname = '存放地点';
        }
    }
    return chname;
}

function getNewEnChList(enlist, chlist, value){
    var list = getEnChList(value);
    var c_len = list[0].length;
    for(var i = 0; i < c_len; i++){
        enlist.push(list[0][i]);
        chlist.push(list[1][i]);
    }
    enlist.push('remark');
    chlist.push('备注信息');
    return [enlist, chlist]
}

function getDefaultEditValue(id, url, value) {
    //  下拉框值从数据库选择,并且设置默认值
    $.ajax({
        "dataType": 'json',
        "type": "GET",
        "url": url,
        "success": function (resp) {
            $("#" + id).find("option").remove();
            var r_len = resp.length;
            for (var i = 0; i < r_len; i++) {
                if (resp[i].ch_name == '报废中'
                    || resp[i].ch_name == '报废无') {
                    continue;
                }
                var opstr = $.parseStr('<option value="%s">%s</option>', resp[i].ch_name, resp[i].ch_name);
                if (resp[i].ch_name == value) {
                    opstr = $.parseStr('<option value="%s" selected="selected">%s</option>', resp[i].ch_name, resp[i].ch_name);
                }
                $("#" + id).append(opstr);
            }
        }
    });
}


function getNeedSelectValue(id, url, value, except) {
    //  下拉框值从数据库选择,并且设置默认值
    $.ajax({
        "dataType": 'json',
        "type": "GET",
        "url": url,
        "success": function (resp) {
            $("#" + id).find("option").remove();
            var opstr = $.parseStr('<option value="%s" selected="selected">%s</option>', value, value);
            $("#" + id).append(opstr);
            var r_len = resp.length;
            for (var i = 0; i < r_len; i++) {
                if(resp[i].ch_name == except){
                    continue;
                }
                opstr = $.parseStr('<option value="%s">%s</option>', resp[i].ch_name, resp[i].ch_name);
                $("#" + id).append(opstr);
            }
        }
    });
}


function getNeedDefaultSelectValue(id, url, value) {
    //  下拉框值从数据库选择,并且设置默认值
    $.ajax({
        "dataType": 'json',
        "type": "GET",
        "url": url,
        "success": function (resp) {
            $("#" + id).find("option").remove();
            var r_len = resp.length;
            for (var i = 0; i < r_len; i++) {
                if (resp[i].ch_name != value) {
                    continue;
                }
                var opstr = $.parseStr('<option value="%s" selected="selected">%s</option>', resp[i].ch_name, resp[i].ch_name);
                $("#" + id).append(opstr);
            }
        }
    });
}

//高级查询资产状态为在用，出库原因去掉资产调拨，如果是库存，增加资产调拨
function getAdvancedInSelectValue(id, url, value) {
    //  下拉框值从数据库选择,并且设置默认值
    $.ajax({
        "dataType": 'json',
        "type": "GET",
        "url": url,
        "success": function (resp) {
            $("#" + id).find("option").remove();
            var opstr = $.parseStr('<option value="%s" selected="selected">%s</option>', value, value);
            $("#" + id).append(opstr);
            var r_len = resp.length;
            for (var i = 0; i < r_len; i++) {
                opstr = $.parseStr('<option value="%s">%s</option>', resp[i].ch_name, resp[i].ch_name);
                $("#" + id).append(opstr);
            }
            opstr = $.parseStr('<option value="%s">%s</option>', "资产调拨", "资产调拨");
            $("#" + id).append(opstr);
        }
    });
}