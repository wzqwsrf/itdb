/**
 * Created by zhenqingwang on 10/27/14.
 */

function initPhoneOutDiv() {
    //  给查询按钮赋值
    var content = constructPhoneRight();
    $('#phone_info_right').append(content);
    initPhoneConsumeOutDom();
    getSelectValue('store_place_p', '/asset_info/loadstate/3', '请选择存放地点');
    getSelectValue('p_store_place', '/asset_info/loadstate/3', '请选择办公地点');
    getNeedSelectValue('p_in_out_reason', '/asset_info/loadstate/5', '请选择出库原因', "资产调拨");
    $('#store_states').val('库存');
    //键盘搜索
    createPhoneFormValidate($("#phone_info_right").find("form"));
}

function constructPhoneRight() {
    var id = 'phone_template';
    var enlist = getPhoneOutRightEnList();
    var chlist = getPhoneOutRightChList();
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
    var num = $('#phone_have_info').find("input[name='num']").val();
    if(num == 0){
        showFailTips("电话号码个数为0,不能出库,请检查!");
        return;
    }
    var thisForm = $("#phone_info_right").find("form");
    if (!thisForm.valid()) {
        return;
    }
    var params = {};
    params['phone_no'] = $('#phone_no_p').val();
    params['store_place'] = $('#p_store_place').val();
    params['in_out_reason'] = $('#p_in_out_reason').val();
    params['remark'] = $('#phone_info_right').find("textarea[name='p_remark']").val();
    $.ajax({
        type: "POST",
        url: "/asset_phone/out/data",
        dataType: "json",
        data: params,
        success: function (resp) {
            if (resp.success) {
                showSuccessTips(resp.msg);
                if (!isGoOn) {
                    // 清空表单
                    thisForm[0].reset();
                    $("#search_phone").val("");
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

            p_store_place: {
                required: true
            },
            p_in_out_reason: {
                required: true
            },
            p_remark: {
                required: true
            }

        },
        messages: {
            p_store_place: {
                required: "请选择一个存放地点"
            },
            p_in_out_reason: {
                required: "请选择入库原因"
            },
            p_remark: {
                required: "请填写备注信息，出库给哪个话机"
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

function initPhoneConsumeOutDom() {
    /*
     * 初始化ztree
     */
    window.zTree;
    window.setting = {
        view: {
            dblClickExpand: false,
            selectedMulti: false,
            showTitle: false,
            showIcon: true
        },
        data: {
            keep: {
                parent: false,
                leaf: false
            },
            simpleData: {
                enable: true,
                idkey: 'id',
                pIdKey: 'pId',
                rootPId: 0
            }
        },
        callback: {
            onClick: getSelectPhoneLtreeNode
        }
    };
    loadTypeList("asset_type_tree_c", 2);
    loadTypeList("asset_type_tree_p", 3);

}


function getSelectPhoneLtreeNode(event, treeId, treeNode) {
    /*
     * @parm:event    : 标准的js event对象
     * @parm:treeId   : 对应ztree的treeId，便于用户操控
     * @parm:treeNode : 被点击的节点json数据对象
     *                  格式：Object {pId: 4, id: 7, name: "笔记本", level: 2, tId: "asset_type_tree_9"…}
     */
    if (treeNode && !treeNode.noR) {
        var assetTypePath = getNodePath(treeNode);
        var assetTypeVal = treeNode.name;
        window.c_tree_id = treeNode.id;

        // 判断是否有子节点
        var arrNodes = treeNode.children;
        $("#asset_type_p").val(assetTypeVal);
        $("#asset_type_c").val(assetTypeVal);

        if(containsValue(consumePeopleList(), assetTypeVal)){
            $('#consume_info_right').empty();
            initActualConsumeOutDiv(getConsumeOutPeopleRightEnList(), getConsumeOutPeopleRightChList());
        }else if(containsValue(consumeAssetList(), assetTypeVal)){
            $('#consume_info_right').empty();
            initActualConsumeOutDiv(getConsumeOutAssetRightEnList(), getConsumeOutAssetRightChList());
        }

        // 使其自定义校验生效
        if (!arrNodes) {
            //说明：当选择没有父节点时，才将得到的值加进input中
            /*
             * 每次选择资产类别时，每点击一个节点，就将对应的品牌select框清除再创建
             * 防止品牌累加
             */
        }
        $('#store_place_p').change(function () {
            $("#phone_no_p").find("option").remove();
            if ($('#store_place_p').val().substr(0, 1) != "请") {
                getReturnPhoneParams(assetTypeVal);
            }
        });

//        $('#asset_type_p').change(function () {
//            $("#phone_no_p").find("option").remove();
//            if ($('#store_place_p').val().substr(0, 1) != "请") {
//                getReturnParams(assetTypeVal);
//            }
//        });

        postSelectValue('provider_c', '/asset_info/prov/types', assetTypeVal, '请选择品牌');
        $('#provider_c').change(function () {
            var proVal = $('#provider_c').val();
            postSelectValue('model_c', '/asset_info/model/types', assetTypeVal + '_' + proVal, '请选择型号');
        });
        getSelectValue('store_place_c', '/asset_info/loadstate/3', '请选择存放地点');

        $('#store_place_c').change(function () {
            if ($('#provider_c').val().substr(0, 1) != "请"
                && $('#model_c').val().substr(0, 1) != "请"
                && $('#store_place_c').val().substr(0, 1) != "请") {
                getReturnConsumeParams(assetTypeVal);

            }
        });
    }
}

function getReturnPhoneParams(assetTypeVal) {
//                getReturnParams();
    var params = {};
    params['asset_type'] = assetTypeVal;
    params['store_place'] = $('#store_place_p').val();
    $.ajax({
        "dataType": 'json',
        "type": "POST",
        "url": '/asset_phone/out',
        'data': params,
        "success": function (resp) {
            var count = resp.count;
            $('#phone_have_info').find("input[name='num']").val(count);
            if (count != 0) {
                var data = resp.data;
                $("#phone_no_p").find("option").remove();
                for (var i = 0; i < count; i++) {
                    var opstr = $.parseStr('<option value="%s">%s</option>', data[i], data[i]);

                    $("#phone_no_p").append(opstr);
                }
            }
        },
        error: function (resp) {
            console.log(resp);
        }
    });
}

function getReturnConsumeParams(assetTypeVal) {
    var params = {};
    params['asset_type'] = assetTypeVal;
    params['store_place'] = $('#store_place_c').val();
    params['provider'] = $('#provider_c').val();
    params['model'] = $('#model_c').val();
    $.ajax({
        "dataType": 'json',
        "type": "POST",
        "url": '/asset_consume/consume/num',
        'data': params,
        "success": function (resp) {
            if ('in_num1' in resp) {//有数据
                $("#consume_have_info").find("input[name='num']").val(resp['in_num1']);
            }
        },
        error: function (resp) {
            console.log(resp);
        }
    });
}