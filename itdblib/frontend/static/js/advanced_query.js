/**
 * Created by zhenqingwang on 10/21/14.
 */

$.extend(true, $.fn.dataTable.defaults, {

    "sPaginationType": "bootstrap",
    "oLanguage": {
        "sEmptyTable": "无数据",
        "sProcessing": "正在获取数据，请稍后...",
        "oPaginate.sFirst": "第一页",
        "oPaginate.sLast": "最后一页",
        "oPaginate.sNext": "下一页",
        "oPaginate.sPrevious": "上一页",
        "sInfo": "本页 _START_ - _END_ , 共 _TOTAL_ 条记录",
        "sInfoEmpty": "本页 0 - 0 , 共 0 条记录",
        "sSearch": "搜索: ",
        "sLengthMenu": "共_MENU_记录"
    }
});
function advance_query(url, num) {

    $('#head_in').append($('#head').show());
    $('#right_in').append($('#right').show());
    $('#query').append($("#query_button").show());
    var placeholder = "请输入资产编号或SN或mac地址或rtx_id或员工编号";
    if (num == 2) {
        placeholder = "请输入rtx_id";
    } else if (num == 3) {
        placeholder = "请输入电话号码";
        document.getElementById("s_provider").style.visibility = "hidden";
        document.getElementById("s_model").style.visibility = "hidden";
    }
    $('#search_val').attr("placeholder", placeholder);
    $('#ad_id').click(function () {
        var anotherDiv = document.getElementById("another_query").style.display;
        if (anotherDiv == "none") {
            document.getElementById("another_query").style.display = "";
            $("#ztree").append(assetTypeDiv());
            initQueryDom(num);
            getSelectValue('s_device_state', '/asset_info/loadstate/1', '请选择设备状态');
            getSelectValue('s_store_state', '/asset_info/loadstate/2', '请选择资产状态');
            getSelectValue('s_store_place', '/asset_info/loadstate/3', '请选择存放地点');
            $('#s_store_state').change(function () {
                if ($("#s_store_state").val() == '库存') {
                    $("#in_out").empty();
                    var content = getAdvancedInOutReason("in", "入库原因", "s_in_reason");
                    $("#in_out").append(content).show();
                    getAdvancedInSelectValue('s_in_reason', '/asset_info/loadstate/4', '请选择入库原因');
                }

                if ($("#s_store_state").val() == '在用') {
                    $("#in_out").empty();
                    var content = getAdvancedInOutReason("out", "出库原因", "s_out_reason");
                    $("#in_out").append(content).show();
                    getNeedSelectValue('s_out_reason', '/asset_info/loadstate/5', '请选择出库原因', '资产调拨');
                }
            });

            $("#s_date_from1").on('click', function () {
                WdatePicker({dateFmt: 'yyyy-MM-dd HH:mm:ss'});
            });
            $("#s_date_to1").on('click', function () {
                WdatePicker({dateFmt: 'yyyy-MM-dd HH:mm:ss'});
            });
            $("#s_date_from2").on('click', function () {
                WdatePicker({dateFmt: 'yyyy-MM-dd HH:mm:ss'});
            });
            $("#s_date_to2").on('click', function () {
                WdatePicker({dateFmt: 'yyyy-MM-dd HH:mm:ss'});
            });
            $('#actual_id').click(function () {
                var list1 = getAdvancedList();
                var params = getAdvancedValues(list1);
                if (detemineAllIsNull(list1, params)) {
                    showFailTips("所有查询条件否为空,请检查");
                } else {
                    showAllInfo(url, params, num);
                }
            });
            $(this).text('收起更多查询条件');
        } else {
            document.getElementById("another_query").style.display = "none";
            $(this).text('展开更多查询条件');
        }
    });
}

function getAdvancedInOutReason(id1, name, id2) {
    var content = '<div class="space-4"></div>';
    content += $.parseStr('<div id="%s">', id1);
    content += $.parseStr('<label  style="width: 98px;"> %s：</label>', name);
    content += $.parseStr('<select id="%s" class="query_s">', id2);
    content += '</select>';
    content += '</div>';
    return content;
}

function getAdvancedValues(list1) {
    var params = {};
    var len1 = list1.length;
    for (var i = 0; i < len1; i++) {
        var value = $("#s_" + list1[i]).val();
        if (isNull(value) || value.substr(0, 1) == "请") {
            value = "";
        }
        params[list1[i]] = value;
    }
    return params;
}


function detemineAllIsNull(list1, params) {
    var len1 = list1.length;
    for (var i = 0; i < len1; i++) {
        if (params[list1[i]] != "") {
            return false;
        }
    }
    return true;
}

function showOperaInfo(phone) {
    var ex = document.getElementById('ope_table');
    if ($.fn.dataTable.fnIsDataTable(ex)) {
        $(ex).dataTable().fnDestroy();
    }
    var aoColumns = [
        {
            "sTitle": "操作类型", "sName": "oper_type", "sClass": "align-center align-middle"
        },
        {
            "sTitle": "操作人/时间", "sName": "operator", "sClass": "align-center align-middle"
        },
        {
            "sTitle": "操作内容", "sName": "text", "sClass": "align-center align-middle"
        }
    ];
    var oTable = $(ex).dataTable({
        "bRetrieve": true,
        "bPaginate": false,
        "bServerSide": false,
        "aoColumns": aoColumns,
        "iDisplayLength": 30,
        "sAjaxSource": "",
        "bAutoWidth": false, //自适应宽度
        "bSort": false,
        "fnServerData": function (sSource, aDataSet, fnCallback) {
            $.ajax({
                "dataType": 'json',
                "type": "GET",
                "url": "operate/" + phone,
                "data": aDataSet,
                "success": function (resp) {
                    var data = showDetailsInfo(resp);
                    fnCallback(data);
                },
                error: function () {
                    $('#show_op_log').html('网络错误');
                }
            });
        }
    });
}

//展示操作信息
function showDetailsInfo(resp) {
//    id | asset_id | time | type | operator | text | filed_value
    var aaData = [];
    d = {};
    if (resp) {
        var d = resp;
        var d_len = d.length;
        for (var i = 0; i < d_len; i++) {
            var text = constructText(d[i]['text'], d[i]['before_field'], d[i]['after_field']);
            aaData.push([
                d[i]['oper_type'],
                textCenter(d[i]['operator'] + '于', d[i]['oper_time'] + '操作'),
                text
            ]);
        }
    }
    var data = {
        "aaData": aaData
    };
    return data;
}

function textCenter(value1, value2) {
    return $.parseStr('<dd><span style="color:blue">%s</span></dd>' +
        '<dd><span style="color:green">%s</span></dd>', value1, value2);
}

function constructText(text, field1, field2) {
    if (isNull(text)) {
        var valueMsg = addNextLine(field1, field2);
        var content = '<table>'
        content += '<tr>';
        content += '<th>修改前</th>';
        content += '<th>修改后</th>';
        content += '</tr>';
        content += '<tr>';
        content += '<th>';
        content += valueMsg[0];
        content += '</th>';
        content += '<th>';
        content += valueMsg[1];
        content += '</th>';
        content += '</tr>';
        content += '</table>';
        return content;
    }
    return text;
}

function addNextLine(value1, value2) {
    if (isNull(value1) || isNull(value2)) {
        return [value1, value2];
    }
    var valueMsg1 = value1.split(",");
    var valueMsg2 = value2.split(",");
    var d_len = Math.min(valueMsg1.length, valueMsg2.length);
    var content1 = "";
    var content2 = "";
    for (var i = 0; i < d_len; i++) {
        if (valueMsg1[i] != valueMsg2[i]) {
            content1 += $.parseStr('<dt><span style="color: green">%s</span><span style="color: red">%s</span></dt>',
                valueMsg1[i].split(":")[0] + ":", valueMsg1[i].split(":")[1]);
            content2 += $.parseStr('<dt><span style="color: green">%s</span><span style="color: red">%s</span></dt>',
                valueMsg2[i].split(":")[0] + ":", valueMsg2[i].split(":")[1]);
        } else {
            content1 += $.parseStr('<dt>%s</dt>', valueMsg1[i]);
            content2 += $.parseStr('<dt>%s</dt>', valueMsg2[i]);
        }
    }
    return [content1, content2];
}

function getAdvancedList() {
    var list = ["store_state", "store_place", "device_state", "in_reason",
        "out_reason", "asset_type", "provider", "model",
        "date_from1", "date_to1", "date_from2", "date_to2", "oper_name"];
    return list;
}

function showAllInfo(url, params, num) {
    if (num == 1) {
        showInfo(url, params);
    } else if (num == 2) {
        showConsumeInfo(url, params);
    } else if (num == 3) {
        showPhoneInfo(url, params);
    }
}

function exportAsset() {
    $('#ex_dev_btn').click(
        function () {
            var form = $("<form>");//定义一个form表单
            form.attr("style", "display:none");
            form.attr("target", "");
            form.attr("method", "post");
            form.attr("action", "export/asset");
            var input1 = $("<input>");
            input1.attr("type", "hidden");
            input1.attr("name", "exportData");
            var value = "";
            if (!isNull($('#search_val').val())) {
                value = $('#search_val').val();
            } else {
                if (document.getElementById("another_query").style.display != "none") {
                    var list1 = getAdvancedList();
                    var params = getAdvancedValues(list1);
                    var len = list1.length;
                    for (var i = 0; i < len; i++) {
                        value += list1[i] + "=" + params[list1[i]] + ","
                    }
                    value = value.substr(0, value.length - 1);
                }
            }
            input1.attr("value", value);
            $("body").append(form);//将表单放置在web中
            form.append(input1);
            form.submit();//表单提交
        }
    );
}