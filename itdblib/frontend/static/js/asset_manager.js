/**
 * Created by zhenqingwang on 8/1/14.
 */

//构建资产信息显示模版
function constructEditAssetDiv(enlist, chlist, store_state) {

    var content = '<form id="edit_valid">';
    var d_len = chlist.length;
    var mid = Math.round(d_len / 2);
    for (var i = 0; i < 2; i++) {
        content += '<div class="col-xs-6">';
        var start = 0;
        var end = mid;
        if (i == 1) {
            start = mid;
            end = d_len;
        }
        for (var j = start; j < end; j++) {
            var chname = transformDivName(chlist[j], store_state);
            content += '<div class="col-xs-w">';
            content += '<label>　　　</label>';
            content += $.parseStr('<label style="width: 80px; height: 21px">%s:</label>', chname);
            if (isSelect((enlist[j]))) {
                content += $.parseStr('<select id="%s" style="width: 180px;height: 28px"></select>', enlist[j] + 's');
            } else {
                if (readOnlyValue(enlist[j])) {
                    content += $.parseStr('<input type="text" id="%s" readonly="true">', enlist[j] + 's');
                } else {
                    content += $.parseStr('<input type="text" id="%s">', enlist[j] + 's');
                }
                content += '<label>　　　　　　</label>';
            }
            content += '</div>';
        }
        content += '</div>';
    }
    content += '</form>';
    return content;
}


//是否为select
function isSelect(value) {

    if (value == 'provider'
        || value == 'model'
        || value == 'device_state'
        ) {
        return true;
    }
    return false;
}

function readOnlyValue(value) {
    if (value == 'asset_id'
        || value == 'asset_type'
        || value == 'in_out_reason'
        || value == 'store_state'
        || value == 'user_name'
        || value == 'store_place'
        ) {
        return true;
    }
    return false;
}

