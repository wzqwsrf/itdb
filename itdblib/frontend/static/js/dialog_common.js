/**
 * Created by zhenqingwang on 11/6/14.
 */
function showCommonNoticeDialog(header, header_icon, msg, width) {
    $("#common-notice-dialog").empty();
    $("#common-notice-dialog").append(msg);
    var title_html_str = $.parseStr('<div class="dialog_title"><li class="%s"></li> %s</div>', header_icon, header);
    var dialog = $("#common-notice-dialog").removeClass('hide').dialog({
        modal: true,
        width: width,
        resizable: true,
        title: title_html_str,
        title_html: true,
        closeOnEscape: false,
        open: function (event, ui) {
            $(".ui-dialog-titlebar-close").hide();
        },
        buttons: [
            {
                text: "确定",
                "class": "btn btn-primary btn-xs",
                click: function () {
                    $("#common-notice-dialog").empty();
                    $("#common-notice-dialog").dialog('destroy');
                }
            }
        ],
        close: function () {
            $("#common-notice-dialog").empty();
            $("#common-notice-dialog").dialog('destroy');
        }
    });
    $(dialog).parent().find('a.ui-dialog-titlebar-close').remove();
}


function generateNoticeMsg(msg) {
    return $.parseStr('<div class="alert alert-info bigger-110" style="margin-bottom: 0px; margin-top: 5px;">%s</div>', msg);
}

function showSuccessTips(msg) {
    showCommonNoticeDialog('成功', 'icon-ok',
        generateNoticeMsg(msg), 300);
}

function showFailTips(msg) {
    showCommonNoticeDialog('失败', 'icon-warning-sign',
        generateNoticeMsg(msg), 300);
}

function showErrorTips() {
    showCommonNoticeDialog('网络错误', 'icon-bolt',
        generateNoticeMsg('网络错误，请刷新后重试!'), 300);
}
