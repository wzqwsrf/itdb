/**
 * Created by zhenqingwang on 10/27/14.
 */

function initPhoneInDiv() {
    //  给查询按钮赋值
    var content = constructPhoneRight();
    $('#phone_info_right').append(content);
//    addValueToSelect(0);
    getSelectValue('p_store_place', '/asset_info/loadstate/3', '请选择存放地点');
    autoShowInfo('phone_info_right', 'p_user_name');
    $('#p_store_place').change(function () {
        if ($('#p_store_place').val().substr(0, 1) != "请") {
            getAdminNameByStorePlace($('#p_store_place').val(), 'phone_info_right', 'p_user_name');
        }
    });
    getSelectInValue('p_in_out_reason', '/asset_info/loadstate/4', '请选择入库原因');
    getSelectInValue('p_device_state', '/asset_info/loadstate/1', '请选择设备状态');
    $('#store_states').val('库存');
    //键盘搜索
    $("#search_phone").keydown(function (e) {
        if (e.keyCode == 13) {
            showAssetInfoById('search_phone', '/asset_info/phone/id',
                'phone_have_info', 0, 3);
        }
    });

    //查询按钮操作
    $('#query_phone').click(function (e) {
        e.preventDefault();
        var param = $("#search_phone").val().replace(/[\s+\t+]+/ig, "");
        if (isNull(param)) {
            showTips(3, "查询条件为空，请检查！");
            return;
        }
        showAssetInfoById('search_phone', '/asset_info/phone/id',
            'phone_have_info', 0, 3);
    });
    createPhoneFormValidate($("#phone_info_right").find("form"));
    skipPhoneToStock('old-p-add');

}

//============资产管理跳转过来代码=========
function skipPhoneToStock(id) {
    var url = location.search;
    if (url.indexOf('phone_no') != -1) {
        var asset_id = url.split('=')[1];
        var value = $.parseStr('ul_tab li>a[href=#%s]', id);
        $("#" + value).trigger('click');
        $("#search_phone").val(asset_id);
        showAssetInfoById('search_phone', '/asset_info/phone/id',
            'phone_have_info', 0, 3);
    }
}

function constructPhoneRight() {
    var id = 'phone_template';
    var enlist = getPhoneRightEnList();
    var chlist = getPhoneRightChList();
    var content = '<form>';
    content += phoneRightForm(id, chlist, enlist);
    content += '</form>';
    return content;
}


function phoneRightForm(id, chlist, enlist) {
    //构造新增入库模版
    var content = $.parseStr('<div id="%s">', id);
    var d_len = chlist.length;
    for (var i = 0; i < d_len; i++) {
        var value = enlist[i];
        content += '<div class="form-group">';
        content += $.parseStr('<label class="col-xs-2 control-label no-padding-right" for="%s">%s：</label>',
            value, chlist[i]);
        content += '<div class="col-xs-9">';
        var in_content = '';
        var actual_value = enlist[i].substr(2);
        if (actual_value == 'remark') {
            in_content = $.parseStr('<textarea name="%s" class="col-xs-12" style="height:100px;"></textarea>',
                value);
        } else if (actual_value == 'asset_type') {
            in_content = assetTypeDiv(enlist[i], "asset_type_tree");
        } else {
            if (isSelect(actual_value)) {
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

function submitPhoneFormRight(isGoOn) {
    console.log(1);
    var thisForm = $("#phone_info_right").find("form");
    if (!thisForm.valid()) {
        return;
    }
    if (isNull($('#search_phone').val())) {
        showFailTips('还没有选择数据，无法出入库');
        return;
    }
    var postData = $("#stock_phone_device").find("form").serializeArray();
    var bData = formatbData(postData);
    bData['p_device_state'] = $('#p_device_state').val();
    if (bData['p_store_state'] == undefined) {
        bData['p_store_state'] = bData['store_state']
    }
    if (bData['p_device_state'] == undefined) {
        bData['p_device_state'] = bData['device_state']
    }
    if (bData['store_state'] == '库存') {
        bData['p_store_state'] = '在用'
    } else if (bData['store_state'] == '在用') {
        bData['p_store_state'] = '库存'
    }
    console.log(2);
//      这里是记录操作日志变更
    formatPhoneOldOperInfo(bData);
    $.ajax({
        type: "POST",
        url: "/asset_phone/old/add",
        dataType: "json",
        data: bData,
        success: function (resp) {
            if (resp.success) {
                var value = $("#search_phone").val();
//                window.location.href = "asset_phone/asset_phone?phone=" += value;
                showSuccessTips(resp.msg);
                if (!isGoOn) {
                    // 清空表单
                    thisForm[0].reset();
                    $("#search_phone").val("");
//                    window.location.href='/asset_phone/asset_phone';
                }
                location.reload();
            } else {
                showFailTips(resp.msg)
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            showErrorTips();
        }
    });
}

function formatPhoneOldOperInfo(aData) {
    var enlist = getPhoneInfoOldEnlist();
    var d_len = enlist.length;
    var before_val = "";
    var after_val = "";
    var rightList = getPhoneRightEnList();
    for (var i = 0; i < d_len; i++) {
        before_val += enlist[i] + ":" + aData[enlist[i]] + ",";
        if (containsValue(rightList, 'p_' + enlist[i]) || enlist[i] == 'store_state') {
            after_val += enlist[i] + ":" + aData['p_' + enlist[i]] + ",";
        } else {
            after_val += enlist[i] + ":" + aData[enlist[i]] + ",";
        }
    }
    var params = {};
    var asset_id = 'phone_no';
    params['asset_id'] = $("#phone_have_info").find("input[name='" + asset_id + "']").val();
    params['oper_type'] = "字段变更";
    params['text'] = "";
    params['before_field'] = before_val;
    params['after_field'] = after_val;
    console.log(params);
    saveOperInfo(params);
}

function createPhoneFormValidate(form) {
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

            p_device_state: {
                required: true
            },
            p_user_name: {
                required: true
            },

            p_store_place: {
                required: true
            },
            p_store_state: {
                required: true
            },
            p_in_out_reason: {
                required: true
            }

        },
        messages: {
            p_device_state: {
                required: "请选择资产状态"
            },
            p_user_name: {
                required: "使用人不能为空"
            },
            p_store_place: {
                required: "请选择一个存放地点"
            },
            p_in_out_reason: {
                required: "请选择入库原因"
            },
            p_store_state: {
                required: "请选择设备状态"
            },
            p_asset_type: {
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