/**
 * Created by zhenqingwang on 10/27/14.
 */

function initConsumeInDiv() {
    //  给查询按钮赋值
    var content = constructConsumeRight();
    $('#consume_info_right').append(content);
    getSelectValue('c_store_place', '/asset_info/loadstate/3', '请选择存放地点');

    $('#c_store_place').change(function () {
        if ($('#c_store_place').val().substr(0, 1) != "请") {
            var list = ["asset_type", "provider", "model", "user_name"];
            var params = {};
            for (var i = 0; i < 4; i++) {
                params[list[i]] = $("#" + list[i] + "_c").val();
            }
            params["store_place"] = $("#c_store_place").val();
            $.ajax({
                "dataType": 'json',
                "type": "POST",
                "url": "consume/num",
                'data': params,
                "success": function (resp) {
                    if ('user_name' in resp) {//有数据
                        $("#consume_info_right").find("input[name='c_user_name']").val(resp['user_name']);
                        $('#consume_info_right').find("input[name='c_user_name']").attr("readonly", "true");
                    }
                },
                error: function (resp) {
                    showErrorTips();
                }
            });
        }
    });

    $('#c_store_place').change(function () {
        if ($('#c_store_place').val().substr(0, 1) != "请") {
            getAdminNameByStorePlace($('#c_store_place').val(), 'consume_info_right', 'c_user_name');
        }
    });

    autoShowInfo('consume_info_right', 'c_user_name');

    getSelectInValue('c_in_out_reason', '/asset_info/loadstate/4', '请选择入库原因');
    getSelectInValue('c_device_state', '/asset_info/loadstate/1', '请选择设备状态');

    createConsumeFormValidate($("#consume_info_right").find("form"));
}


function constructConsumeRight() {
    var id = 'consume_template';
    var enlist = getConsumeRightEnList();
    var chlist = getConsumeRightChList();
    var content = '<form>';
    content += consumeRightForm(id, chlist, enlist);
    content += '</form>';
    return content;
}


function consumeRightForm(id, chlist, enlist) {
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

function submitConsumeInFormRight(isGoOn) {
    var thisForm = $("#consume_info_right").find("form");
    if (!thisForm.valid()) {
        return;
    }
    var postData = $("#stock_consume_device").find("form").serializeArray();
    var bData = formatbData(postData);
    var right_num = bData['c_in_num'];
    var left_num = $("#in_num_c").val();
    if (parseInt(right_num) > parseInt(left_num)) {
        showFailTips("入库数量大于使用数量，请检查");
        return;
    }
    bData['c_device_state'] = $('#c_device_state').val();
    if (bData['c_store_state'] == undefined) {
        bData['c_store_state'] = bData['store_state']
    }
    if (bData['c_device_state'] == undefined) {
        bData['c_device_state'] = bData['device_state']
    }
    bData['asset_type'] = $('#asset_type_c').val();
    bData['model'] = $('#model_c').val();
    bData['provider'] = $('#provider_c').val();
    bData['c_store_state'] = '库存';
//      这里是记录操作日志变更

    $.ajax({
        type: "POST",
        url: "/asset_consume/old/add",
        dataType: "json",
        data: bData,
        success: function (resp) {
            var id = resp.msg;
            var msg = resp.msg;
            if (msg == -1) {
                msg = "添加耗材类数据失败！";
            }
            if (!isNaN(msg)) {
                msg = "添加耗材类数据成功！";
            }
            if (resp.success) {
                showSuccessTips(msg);
                if (!isGoOn) {
                    // 清空表单
                    thisForm[0].reset();
                    $("#search_consume").val("");
                }
                location.reload();
                //formatConsumeOldOperInfo(bData, id);
            } else {
                showFailTips(msg)
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            showErrorTips();
        }
    });
}

function formatConsumeOldOperInfo(aData, consumeId) {
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
    before_val += "id" + ":" + consumeId + ",";
    after_val += "id" + ":" + consumeId + ",";
    var params = {};
    params['asset_id'] = consumeId;
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
            c_in_num: {
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
            c_in_out_reason: {
                required: true
            }

        },
        messages: {
            c_in_num: {
                required: "入库数量不能为空"
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