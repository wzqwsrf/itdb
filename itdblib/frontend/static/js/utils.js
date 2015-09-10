/**
 * Created by zhenqingwang on 7/24/14.
 */
//dataTable样式-->


//替换方法
(function ($) {
    $.parseStr = function (str) {
        var args = [].slice.call(arguments, 1),
            i = 0;
        return str.replace(/%s/g, function () {
            return args[i++];
        });
    }
})(jQuery);

function getCurrentMonthStart() {
    var start_time = new Date();
    start_time.setMilliseconds(0);
    start_time.setDate(1);
    start_time.setHours(0);
    start_time.setMinutes(0);
    start_time.setSeconds(0);
    return start_time;
}

function containsValue(list, value) {
    var len = list.length;
    for (var i = 0; i < len; i++) {
        if (list[i] == value) {
            return true;
        }
    }
    return false;
}

function hasUserName(user_name) {
    if (isNull(user_name)) {
        return false;
    }
    var flag = true;
    $.ajax({
        type: "POST",
        url: "/asset_info/owner",
        dataType: "json",
        data: {return_val : user_name},
        success: function (resp) {
            console.log(resp);
            if (resp == "员工不存在") {
                flag = false;
                console.log(flag);
                showFailTips("rtx_id不存在，请检查");

            } else {
                showSuccessTips(resp);
            }
            console.log(flag);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            showErrorTips();
        }
    });
    return flag;
}

function autoShowInfo(id, name) {
    $('#' + id).find("input[name='" + name + "']").autocomplete(
        {
            source: function (request, response) {
                $.ajax({
                    url: "/asset_info/auto/show",
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
            minChars: "2"
//        select: function (e, ui) {
//            location.href = "/user/" + ui.item.value;
//        }
        });
}

function getAdminNameByStorePlace(store_place, id, name){
    $.ajax({
        type: "POST",
        url: "/asset_info/admin/name",
        dataType: "json",
        data: {return_val: store_place},
        success: function (resp) {
            var value = resp[0];
            if(isNull(value)){
                value = "库房管理员为空,请手动填写!";
            }
            $('#' + id).find("input[name='" + name + "']").val(value);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            showErrorTips();
        }
    });
}