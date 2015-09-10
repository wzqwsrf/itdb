/**
 * Created by zhenqingwang on 7/28/14.
 */

function constructRight(in_or_out) {
    var id = 'right_template';
    var chlist = [];
    var enlist = [];
    if (in_or_out == 0) { //入库
        chlist = getAssetInfoInChRight();
        enlist = getAssetInfoInEnRight();
    } else { //出库
        chlist = getAssetInfoOutChRight();
        enlist = getAssetInfoOutEnRight();
    }
    var content = '<form>';
    content += constructActualAdd(id, chlist, enlist, 1, in_or_out);
    content += '</form>';
    return content;
}

function addAssetOutRight() {
    var content = '';
    content += '<div class="form-group">';
    content += '<label class="col-xs-2 control-label no-padding-right" for="usage">';
    content += '资产用途：';
    content += '</label>';
    content += '<div class="col-xs-9">';
    content += '<div>';
    content += '<input type="radio" value="办公" name="usage" ' +
    'style="width:40%;!important" onclick="changeOutReason(this)" checked> 办公';
    content += '</div>';
    content += '<div>';
    content += '<input type="radio" value="库存" name="usage" ' +
    'style="width:40%;!important" onclick="changeOutReason(this)"> 库存';
    content += '</div>';
    content += '</div>';
    content += '</div>';
    return content;
}

function addStoreStates() {
    var content = '';
    content += '<div style="display: none">'
    content += '<input id="store_states">';
    content += '</div>';
    return content;
}

function constructNewAssetTypeAdd() {
    var id = 'new_template';
    var chlist = getAssetInfoAssetTypeChlist();
    var enlist = getAssetInfoAssetTypeEnlist();
    return constructActualAdd(id, chlist, enlist, 2, 0);
}
//构造新增入库模版
function constructActualAdd(id, chlist, enlist, num, in_or_out) {

    var content = $.parseStr('<div id="%s">', id);
    if (in_or_out == 1) {
        content += addAssetOutRight();
    }
    if (num == 1) {
        content += addStoreStates();
    }

    var d_len = chlist.length;
    for (var i = 0; i < d_len; i++) {
        if (in_or_out == 1 && num == 1 && enlist[i] == 'device_state') {
            continue;
        }
        var value = enlist[i];
        if (num == 1) {
            value += 's';
        }
        if (enlist[i] == 'in_out_reason') {
            if (in_or_out == 1) {
                chlist[i] = '出库原因';
            } else {
                chlist[i] = '入库原因';
            }
        }
        content += '<div class="form-group">';
        content += $.parseStr('<label class="col-xs-2 control-label no-padding-right" for="%s">%s：</label>',
            value, chlist[i]);
        content += '<div class="col-xs-9">';
        var in_content = '';
        if (enlist[i] == 'remark') {
            in_content = $.parseStr('<textarea name="%s" class="col-xs-12" style="height:100px;"></textarea>',
                value);
        } else if (enlist[i] == 'asset_type') {
            in_content = assetTypeDiv(enlist[i], "asset_type_tree");
        } else if (enlist[i] == 'owner') {
            in_content = $.parseStr('<input class="col-xs-12" type="text" name="%s" placeholder="请输入%s" readonly="true">',
                value, chlist[i]);
        } else if (enlist[i] == 'userful_life') {
            in_content += '<span class="input-icon input-icon-right">';
            in_content += $.parseStr('<input class="col-xs-12" type="text" name="%s" placeholder="请输入%s">',
                value, chlist[i]);
            in_content += '<i class="icon-calendar green"></i>'
            in_content += '</span>';
        } else {
            if (isSelect(enlist[i])) {
                in_content = $.parseStr('<select name="%s" class="chosen-container ' +
                    'chosen-container-single chosen-container-single-nosearch ' +
                    'chosen-with-drop chosen-container-active" ' +
                    'style="width: 0px; margin: 0px 0px 4px;"' +
                    'id="%s"><option value="%s" selected="selected">请选择%s</option></select>',
                    value, value, chlist[i], chlist[i]);
            } else {
                in_content = $.parseStr('<input class="col-xs-12" type="text" name="%s" placeholder="请输入%s">',
                    value, chlist[i]);
            }
        }
        content += in_content;
        content += '</div>';
        content += '</div>';
        content += '<div class="space-4"></div>';

    }
    content += '</div>';
    return content;
}

//是否为select
function isSelect(value) {

    if (value == 'asset_type'
        || value == 'provider'
        || value == 'model'
        || value == 'device_state'
        || value == 'store_place'
        || value == 'store_state'
        || value == 'in_out_reason'
    ) {
        return true;
    }
    return false;
}


//============资产管理跳转过来代码=========
function skipAssetManagerToStock(id, in_or_out) {
    var url = location.search;
    if (url.indexOf('asset_id') != -1) {
        var asset_id = url.split('=')[1];
        var value = $.parseStr('ul_tab li>a[href=#%s]', id);
        $("#" + value).trigger('click');
        $("#search_val").val(asset_id);
        showAssetInfoById('search_val', '/asset_info/asset/id',
            'asset_have_info', in_or_out, 1);
    }
}


///入库和出库初始信息加载
function initStockInOutDiv(in_or_out) {
    var value = '入库信息';
    if (in_or_out == 1) {
        value = '出库信息';
    }
    //  这里是给已有资产入库右栏赋值
    var content1 = constructRight(in_or_out);
    $('#stock_info_right').append(content1);

    $('#right_title').append($.parseStr('<strong> %s </strong>', value));
//  给查询按钮赋值
    $('#query').append($("#query_button").show());
//  给已有资产入库最大的tab赋值
    $('#stock_have_device').append($("#exist_asset").show());
//  样式赋值
    $("#stock_info_right").find("input").removeClass().addClass("col-xs-11");
    $("#stock_info_right").find("textarea").removeClass().addClass("col-xs-11");

//  这里是给已有资产入库左栏赋值
    var content2 = constructAssetDiv(in_or_out, undefined);
    $('#asset_have_info').append(content2);
//  这是给右侧的select框赋值
    addValueToSelect(in_or_out);
    autoShowInfo('right_template', 'user_names');
    //键盘搜索
    $("#search_val").keydown(function (e) {
        if (e.keyCode == 13) {
            showAssetInfoById('search_val', '/asset_info/asset/id',
                'asset_have_info', in_or_out, 1);
        }
    });


    //查询按钮操作
    $('#query_id').click(function (e) {
        e.preventDefault();
        var param = $("#search_val").val().replace(/[\s+\t+]+/ig, "");
        if (isNull(param)) {
            showFailTips("查询条件为空，请检查！");
            return;
        }
        showAssetInfoById('search_val', '/asset_info/asset/id',
            'asset_have_info', in_or_out, 1);
    });
    createFormValidate($("#stock_info_right").find("form"));
    //  资产管理页面链接处理数据
    skipAssetManagerToStock('old-add', in_or_out);
}

function addValueToSelect(in_or_out) {

    getSelectValue('store_places', '/asset_info/loadstate/3', '请选择存放地点');
    if (in_or_out == 1) {
        getNeedSelectValue('in_out_reasons', '/asset_info/loadstate/5', '请选择出库原因', "资产调拨");
        getSelectValue('device_states', '/asset_info/loadstate/1', '请选择设备状态');
        $('#store_states').val('在用');
    } else {
        getSelectInValue('in_out_reasons', '/asset_info/loadstate/4', '请选择入库原因');
        getSelectInValue('device_states', '/asset_info/loadstate/1', '请选择设备状态');
        $('#store_states').val('库存');
        $('#store_places').change(function () {
            if ($('#store_places').val().substr(0, 1) != "请") {
                getAdminNameByStorePlace($('#store_places').val(), 'right_template', 'user_names');
            }
        });
    }


}

//根据搜索加载资产库存信息
function showAssetInfoById(searchId, url, formId, in_or_out, num) {
    var searchVal = $("#" + searchId).val();
    $.ajax({
        type: "POST",
        url: url,
        dataType: "json",
        data: {return_val: searchVal},
        success: function (resp) {
            var retDict = resp[0];
            var enlist = [];
            if (num == 1) {
                var asset_type = retDict['asset_type'];
                //  这里是给已有资产入库左栏赋值
                $('#asset_have_info').empty();
                var content2 = constructAssetDiv(in_or_out, asset_type);
                $('#asset_have_info').append(content2);
                var chlist = getAssetInfoOldChlist();
                var enlist = getAssetInfoOldEnlist();
                var list = getNewEnChList(enlist, chlist, asset_type);
                enlist = list[0];
            } else if (num == 2) {
                enlist = getConsumeInfoOldEnlist();
            } else if (num == 3) {
                enlist = getPhoneInfoOldEnlist();
            }

            var d_len = enlist.length;
            for (var i = 0; i < d_len; i++) {
                $("#" + formId).find("input[name='" + enlist[i] + "']").val(retDict[enlist[i]]);
            }
//          限制资产状态为在用，无法出库//资产状态为库存，无法入库，请知悉
            if (in_or_out == 1) {
                if (retDict['store_state'] == '在用') {
                    showFailTips('资产状态为在用，无法出库，请知悉');
                    disabledStockRight();
                }
                if (retDict['device_state'] != '可用') {
                    showFailTips('设备状态不可用，无法出库，请知悉');
                    disabledStockRight();
                }
            } else {
                if (retDict['store_state'] == '库存') {
                    showFailTips('资产状态为库存，无法入库，请知悉');
                    disabledStockRight();
                }
            }
        }
    });
}

function disabledStockRight() {
    $("#stock_info_right").find("input").attr("readonly", "true");
    $("#stock_info_right").find("textarea").attr("readonly", "true");
    $("#stock_info_right").find("select").attr("disabled", "true");
}

//构建资产信息显示模版
function constructAssetDiv(in_or_out, asset_type) {
    var chlist = getAssetInfoOldChlist();
    var enlist = getAssetInfoOldEnlist();
    if (!isNull(asset_type)) {
        var list = getNewEnChList(enlist, chlist, asset_type);
        enlist = list[0];
        chlist = list[1];
    }
    var content = '';
    var d_len = chlist.length;
    for (var i = 0; i < d_len; i += 2) {
        content += '<div class="form-group">';
        for (var j = i; j < i + 2 && j < d_len; j++) {
            if (chlist[j] == '出入库原因') {
                if (in_or_out == 0) { // 入库 显示上一次的出库原因
                    chlist[j] = '出库原因';
                } else {
                    chlist[j] = '入库原因';
                }
            }
            content += $.parseStr(
                '<label class="col-xs-2 control-label no-padding-right" for="%s">%s：</label>',
                enlist[j], chlist[j]);
            content += $.parseStr(
                '<input type="text" name="%s" class="col-sm-4" readonly=true/>',
                enlist[j]);
        }
        content += '</div>';
    }
    return content;
}

function constructTypeInfo() {
    var content = '<div id="type_info">';
    content += actualTypeInfo('IMEI号', 'imei');
    content += actualTypeInfo('版本号', 'version');
    content += '</div>';
    return content;
}

function actualTypeInfo(chName, enName) {
    var content = '<div class="form-group">';
    content += $.parseStr('<label class="col-xs-2 control-label no-padding-right" ' +
    'for="%s">%s：</label>', enName, chName);
    content += '<div class="col-xs-9">';
    content += $.parseStr('<input class="col-xs-12" type="text" name="%s" placeholder="%s">',
        enName, '请输入' + chName);
    content += '</div>';
    content += '</div>';
    return content;
}

// 根据选择的用途，自动生成对应的出库原因
function changeOutReason(curVal) {
    var selectVal = curVal.value;
    var reason = $("#stock_info_right").find("select[name='in_out_reasons']");
    if (selectVal == '库存') {
        console.log('库存');
        reason.empty();
        getNeedDefaultSelectValue('in_out_reasons', '/asset_info/loadstate/5', '资产调拨');
        $('#store_places').change(function () {
            if ($('#store_places').val().substr(0, 1) != "请") {
                getAdminNameByStorePlace($('#store_places').val(), 'right_template', 'user_names');
            }
        });
    }
    else {
        reason.empty();
        getNeedSelectValue('in_out_reasons', '/asset_info/loadstate/5', '请选择出库原因', '资产调拨');
        //如果是办公,删掉change事件,给user_names赋值为空
        $("#store_places").unbind("change");
        $("#stock_info_right").find("input[name='user_names']").val('');

    }
}

// 表单校验
function createFormValidate(form) {
    /*
     * 添加自定义校验
     */
    jQuery.validator.addMethod("device_type_check", function (value, element) {
        var is_valid = true;
        if (zTree && zTree.getNodeByParam('pId', c_tree_id)) {
            /* 匹配的属性名称为pId
             * 匹配的属性值为c_tree_id
             * 根据当前点击的值，判断是否具有pId这个属性
             */
            is_valid = false;
        }
        return this.optional(element) || is_valid;
    }, $.validator.format("只能选择对应的设备类型"));

    form.validate({
        errorClass: 'error-label',
        focusInvalid: false,
        rules: {
            asset_id: {
                required: true
            },
            sn: {
                required: true
            },
            device_type: {
                required: true
            },
            device_state: {
                required: true
            },
            user_name: {
                required: true
            },
            user_names: {
                required: true
            },
            userful_life: {
                required: true
            },
            store_place: {
                required: true
            },
            in_out_reason: {
                required: true
            },
            provider: {
                required: true
            },
            model: {
                required: true
            },
            asset_type: {
                required: true,
                device_type_check: true
            }
        },
        messages: {
            asset_id: {
                required: "资产编号不能为空"
            },
            sn: {
                required: "SN号不能为空"
            },
            device_type: {
                required: "设备类型不能为空"
            },
            device_state: {
                required: "请选择资产状态"
            },
            user_name: {
                required: "使用人不能为空"
            },
            user_names: {
                required: "使用人不能为空"
            },
            userful_life: {
                required: "有效期限不能为空"
            },
            store_place: {
                required: "请选择一个存放地点"
            },
            in_out_reason: {
                required: "请选择入库原因"
            },
            provider: {
                required: "请选择品牌"
            },
            model: {
                required: "请选择型号"
            },
            asset_type: {
                required: "请选择资产的设备类型"
            }
        },
        errorPlacement: function (error, element) {
            $(element).parent().children(".icon-exclamation").remove();
            var error_dom = $.parseStr('<i class="%s" title="%s"></i>',
                'icon-exclamation tooltip-error', error.html()
            );
            if (element.is('.type_select')) {
                $(error_dom).insertAfter(element.parent().children(":first-child"));
            } else {
                $(error_dom).insertAfter(element.parent().children(":last-child"));
            }
        },
        success: function (label, element) {
            $(element).parent().children(".icon-exclamation").remove();
        }
    });
}

function getActualEnChList(value) {
    var chlist = [];
    var enlist = [];
    if (containsValue(consumeList(), value)) {
        chlist = consume_info_ch_list();
        enlist = consume_info_en_list();
    } else if (containsValue(phoneList(), value)) {
        chlist = phone_info_ch_list();
        enlist = phone_info_en_list();
    } else {
        chlist = getAssetInfoNewChlist();
        enlist = getAssetInfoNewEnlist();
        var list = getEnChList(value);
        chlist = mergeList(chlist, list[1]);
        enlist = mergeList(enlist, list[0]);
    }
    chlist.push("备注信息");
    enlist.push("remark");
    return [enlist, chlist];
}

function construct_exist_asset(all_id, have_info, right_info, button1, button2, button3, name1, name2, in_or_out) {
//    style="display:none"
    var form = '';
    form += $.parseStr('<div id="%s">', all_id);
    form += '<form class="form-horizontal">';
    form += '<div class="row">';
    form += '<div class="col-xs-12">';
    form += '<div class="col-sm-7">';
    form += '<div class="widget-box">';
    form += '<div class="widget-header">';
    form += $.parseStr('<h4 class="header blue"><strong> %s </strong></h4>', name1);
    form += '</div>';
    form += '<div class="widget-body">';
    form += '<div class="widget-main" style="padding:12px 3px 12px 3px;">';
    form += $.parseStr('<div id="%s">', have_info);
//  动态创建左栏内容
    form += constructAssetDiv(in_or_out);
    form += '</div>';
    form += '</div>';
    form += '</div>';
    form += '</div>';
    form += '</div>';
    form += '<div class="col-sm-5">';
    form += '<div class="widget-box">';
    form += '<div class="widget-header">';
    form += $.parseStr('<h4 class="header blue"><strong> %s </strong></h4>', name2);
    form += '</div>';
    form += '<div class="widget-body">';
    form += '<div class="widget-main">';
    form += $.parseStr('<div id="%s">', right_info);
    form += constructRight(in_or_out);
    form += '</div>';
    form += '</div>';
    form += button_div(button1, button2, button3);
    form += '</div>';
    form += '</div>';
    form += '</div>';
    form += '</div>';
    form += '</div>';
    form += '</form>';
    form += '</div>';
    return form;
}

function button_div(id1, id2, id3) {
//     style="display: none"
    var form = '';
    form += $.parseStr('<div class="row" id="%s">', id1);
    form += '<div class="col-xs-12">';
    form += '<div style="float:right;margin-top:20px;margin-bottom:10px; margin-right:11%;">';
    form += $.parseStr('<button class="btn btn-info" type="button" id="%s">', id2);
    form += '<i class="icon-arrow-right bigger-110"></i>提交';
    form += '</button>';
    form += $.parseStr('<button class="btn btn-info" type="button" id="%s">', id3);
    form += '<i class="icon-arrow-up bigger-110"></i>提交并继续';
    form += '</button>';
    form += '<button class="btn" type="reset">';
    form += '<i class="icon-undo bigger-110"></i>重置';
    form += '</button>';
    form += '</div>';
    form += '</div>';
    form += '</div>';
    return form;
}

function formatbData(postData) {
    var a_len = postData.length;
    var bData = {};
    for (var i = 0; i < a_len; i++) {
        bData[postData[i].name] = postData[i].value;
    }
    return bData;
}
