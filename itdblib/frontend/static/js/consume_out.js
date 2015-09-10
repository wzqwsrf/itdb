/**
 * Created by zhenqingwang on 10/27/14.
 */

function initConsumeOutDiv() {

    initPhoneConsumeOutDom();
    initActualConsumeOutDiv(getConsumeOutPeopleRightEnList(), getConsumeOutPeopleRightChList());
}

function initActualConsumeOutDiv(list1, list2) {

    //  给查询按钮赋值
    var content = constructConsumeRight(list1, list2);
    $('#consume_info_right').append(content);
    getSelectValue('c_store_place', '/asset_info/loadstate/3', '请选择存放地点');

    autoShowInfo('consume_info_right', 'c_user_name');

    autoAssetShowInfo('consume_info_right', 'asset_id');

    getNeedSelectValue('c_in_out_reason', '/asset_info/loadstate/5', '请选择出库原因', "资产调拨");

    createConsumeFormValidate($("#consume_info_right").find("form"));
}

function constructConsumeRight(list1, list2) {
    var id = 'consume_template';
    var enlist = list1;
    var chlist = list2;
    var content = '<form>';
    content += consumeRightForm(id, chlist, enlist);
    content += '</form>';
    return content;
}


function consumeRightForm(id, chlist, enlist) {
    //构造新增入库模版
    var content = $.parseStr('<div id="%s">', id);
    content += addConsumeOutRight();
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

function addConsumeOutRight() {
    var content = '';
    content += '<div class="form-group">';
    content += '<label class="col-xs-2 control-label no-padding-right" for="usage">';
    content += '耗材用途：';
    content += '</label>';
    content += '<div class="col-xs-9">';
    content += '<div>';
    content += '<input type="radio" value="办公" name="usage" ' +
    'style="width:40%;!important" onclick="changeConsumeOutReason(this)" checked> 办公';
    content += '</div>';
    content += '<div>';
    content += '<input type="radio" value="库存" name="usage" ' +
    'style="width:40%;!important" onclick="changeConsumeOutReason(this)"> 库存';
    content += '</div>';
    content += '</div>';
    content += '</div>';
    return content;
}


function submitConsumeOutFormRight(isGoOn) {
    var thisForm = $("#consume_info_right").find("form");
    if (!thisForm.valid()) {
        return;
    }
    var postData = $("#stock_consume_device").find("form").serializeArray();
    var bData = formatbData(postData);
    var right_num = bData['c_out_num'];
    var left_num = $("#num_c").val();
    console.log(right_num);
    console.log(left_num);
    if (parseInt(right_num) > parseInt(left_num)) {
        showFailTips("出库数量大于已有数量，请检查");
        return;
    }
    bData['asset_type'] = $('#asset_type_c').val();
    bData['provider'] = $('#provider_c').val();
    bData['model'] = $('#model_c').val();
    bData['in_out_reason'] = bData['c_in_out_reason'];
    bData['store_place1'] = $('#store_place_c').val();
    bData['store_place2'] = bData['c_store_place'];
    bData['out_num'] = bData['c_out_num'];
    if (!isNull(bData['c_user_name'])) {
        bData['user_name'] = bData['c_user_name'];
    } else {
        if (bData['in_out_reason'] != "资产调拨") {
            bData['user_name'] = bData['asset_id'].split('(')[0].toUpperCase();
        } else {
            bData['user_name'] = bData['asset_id'];
        }

    }
    bData['remark'] = bData['c_remark'];
//      这里是记录操作日志变更
//    formatConsumeOldOperInfo(bData);
    $.ajax({
        type: "POST",
        url: "/asset_consume/consume/out",
        dataType: "json",
        data: bData,
        success: function (resp) {
            if (resp.success) {
                showSuccessTips(resp.msg);
                if (!isGoOn) {
                    // 清空表单
                    thisForm[0].reset();
                    $("#search_consume").val("");
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

function formatConsumeOldOperInfo(aData) {
    var enlist = getConsumeInfoOldEnlist();
    var d_len = enlist.length;
    var before_val = "";
    var after_val = "";
    var rightList = getConsumeRightEnList();
    for (var i = 0; i < d_len; i++) {
        before_val += enlist[i] + ":" + aData[enlist[i]] + ",";
        if (containsValue(rightList, 'c_' + enlist[i]) || enlist[i] == 'store_state') {
            after_val += enlist[i] + ":" + aData['c_' + enlist[i]] + ",";
        } else {
            after_val += enlist[i] + ":" + aData[enlist[i]] + ",";
        }
    }
    var params = {};
    var asset_id = 'consume';
    params['asset_id'] = asset_id;
    params['oper_type'] = "字段变更";
    params['text'] = "";
    params['before_field'] = before_val;
    params['after_field'] = after_val;
    saveOperInfo(params);
}

function createConsumeFormValidate(form) {
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
            c_out_num: {
                required: true
            },
            c_device_state: {
                required: true
            },
            c_user_name: {
                required: true
            },
            c_store_place: {
                required: true
            },
            c_store_state: {
                required: true
            },
            asset_id: {
                required: true
            },
            c_in_out_reason: {
                required: true
            }

        },
        messages: {
            c_out_num: {
                required: "出库数量不能为空"
            },
            c_device_state: {
                required: "请选择资产状态"
            },
            c_user_name: {
                required: "使用人不能为空"
            },
            c_store_place: {
                required: "请选择一个存放地点"
            },
            c_in_out_reason: {
                required: "请选择入库原因"
            },
            c_store_state: {
                required: "请选择设备状态"
            },
            c_asset_type: {
                required: "请选择资产的设备类型"
            },
            asset_id: {
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

// 根据选择的用途，自动生成对应的出库原因
function changeConsumeOutReason(curVal) {
    var selectVal = curVal.value;
    var reason = $("#consume_info_right").find("select[name='c_in_out_reason']");
    if (selectVal == '库存') {
        reason.empty();
        getNeedDefaultSelectValue('c_in_out_reason', '/asset_info/loadstate/5', '资产调拨');
        autoShowInfo('consume_info_right', 'asset_id');
        $('#c_store_place').change(function () {
            if ($('#c_store_place').val().substr(0, 1) != "请") {
                getAdminNameByStorePlace($('#c_store_place').val(), 'consume_info_right', 'c_user_name');
            }
        });
    }
    else {
        reason.empty();
        getNeedSelectValue('c_in_out_reason', '/asset_info/loadstate/5', '请选择出库原因', '资产调拨');
        //如果是办公,删掉change事件,给user_names赋值为空
        $("#consume_info_right").find("input[name='asset_id']").val('');
        $("#c_store_place").unbind("change");

    }
}

function autoAssetShowInfo(id, name) {
    $('#' + id).find("input[name='" + name + "']").autocomplete(
        {
            source: function (request, response) {
                $.ajax({
                    url: "/asset_info/auto/id",
                    dataType: "json",
                    type: "POST",
                    data: {
                        return_val: $('#' + id).find("input[name='" + name + "']").val()
                    },
                    success: function (data) {
                        response($.map(data, function (item) {
                            return item;
                        }));
                    }
                });
            },
            dataType: 'json',
            minChars: "5"
//        select: function (e, ui) {
//            location.href = "/user/" + ui.item.value;
//        }
        });
}
