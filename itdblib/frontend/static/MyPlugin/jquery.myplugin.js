(function($){
    $.createMsgTipsFn= function(){
        $("#msg_tips").remove()
        $("body").append('<div id="msg_tips"></div>')
        id = null
        function showTipsIn(type, msg){
            clearTimeout(id)
            $('#msg_tips').hide()
            $('#msg_tips').empty()
            if(type == 1){
                $("#msg_tips").append('<span class="label label-success"><i class="icon-ok bigger-120"></i> ' + msg + '</span>')
            }else if(type == 2){
                $("#msg_tips").append('<span class="label label-warning"><i class="icon-exclamation bigger-120"></i> ' + msg + '</span>')
            }else{
                $("#msg_tips").append('<span class="label label-danger"><i class="icon-exclamation bigger-120"></i> ' + msg + '</span>')
            }
            var width = $('#msg_tips').width()
            $('#msg_tips').css('margin-left', width/(-2) + 'px')
            $('#msg_tips').show()
            id=setTimeout(function(){
                $('#msg_tips').hide()
                $('#msg_tips').empty()
            }, 5000*type)
        }
        return showTipsIn
    }
})(jQuery);

(function($){
    $.parseStr = function(str) {
        var args = [].slice.call(arguments, 1),
        i = 0;
        return str.replace(/%s/g, function() {
            return args[i++];
        });
    }
})(jQuery);

(function($){
    $.stringEncode = function(str){
        var div=document.createElement('div');
        if(div.innerText){
            div.innerText=str;
        }else{
            div.textContent=str;//Support firefox
        }
        return div.innerHTML;
    }

    $.formatStr = function(str){
        var s = $.stringEncode(str)
        if (typeof(str) == 'string'){
            s = str.replace(/\n/g, "<br>");
        }else if(str == null){
            s = '';
        }else{
            s = str;
        } 
        return s
    }
})(jQuery);

(function($){
    Date.prototype.Format = function (fmt) {
        var o = {
            "M+": this.getMonth() + 1, //月份  
            "d+": this.getDate(), //日 
            "H+": this.getHours(), //小时  
            "m+": this.getMinutes(), //分 
            "s+": this.getSeconds(), //秒 
            "q+": Math.floor((this.getMonth() + 3) / 3), //季度  
            "S": this.getMilliseconds() //毫秒  
        };
        if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        for (var k in o) 
            if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        return fmt;
    }

})(jQuery);


(function($){
    var setHeight = function(obj, rh, devi, inrh){
        var wh = $(window).height()
        h = Math.max((wh - rh)*devi/12-inrh, 150)
        obj.css({
            "overflow": "auto",
            "height": h
        })
    }
    // 功能: 
    //
    //
    $.setObjectFull = function(obj, rh, devi, inrh){
        setHeight(obj, rh, devi, inrh)
        $(window).resize(function(){
            setHeight(obj, rh, devi, inrh)
        })
    }
})(jQuery);

(function($){
    var parse = function(str) {
        var args = [].slice.call(arguments, 1),
        i = 0;
        return str.replace(/%s/g, function() {
            return args[i++];
        });
    }
    var defaults = {
        mark_id: 'mark_div',
        mark_tip: 'loading',
    }
    $.fn.mark = function(options){
    var setting = $.extend({}, defaults, options)
    if ($('#' + setting.mark_id).length > 0){
        $('#' + setting.mark_id).show()
        var mark_obj = $('#' + setting.mark_id)
    }else{
        var mark_content = parse('<div id=%s>%s</div>', setting.mark_id,setting.mark_tip)
        this.after(mark_content)
        $('#' + setting.mark_id).addClass('marking')
        var mark_obj = $('#' + setting.mark_id)
        $(window).resize({me_obj: this, mark_obj: mark_obj}, function(e){
            e.data.mark_obj.css({
                "top": e.data.me_obj[0].offsetTop,
                "left": e.data.me_obj[0].offsetLeft,
                "width": e.data.me_obj[0].offsetWidth,
                "height": e.data.me_obj[0].offsetHeight,
                "line-height": e.data.me_obj[0].offsetHeight + 'px' 
            })
        })
        $('#' + setting.mark_id).css({
            "top": this[0].offsetTop,
            "left": this[0].offsetLeft,
            "width":this[0].offsetWidth,
            "height": this[0].offsetHeight,
            "line-height": this[0].offsetHeight + 'px'
        })

    }
    return mark_obj
    }
})(jQuery);

(function($){
    $.fn.serializeObject = function(){
        var o = {};
        var a = this.serializeArray();
        $.each(a, function() {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    }
})(jQuery);

$(function(){
    $(document).tooltip({
        position: {
            my: "center bottom-10",
            at: "center top",
            using: function(position, feedback) {
                $(this).css(position);
                $("<div>")
                .addClass("arrow")
                .addClass(feedback.vertical)
                .addClass(feedback.horizontal)
                .appendTo(this);
            }
        },
        content: function(){
            if($(this).hasClass('tooltip-error')){
                return '<div style="color: red">' + $(this).prop('title') + '</div>';
            }else{
                return $(this).prop('title');
            }
        },
        hide: {'duration': 300}
    });
});

