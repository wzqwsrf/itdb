/**
 * Created by zhenqingwang on 8/18/14.
 */

function assetTypeDiv(id, ulId) {
    var in_content = $.parseStr('<input type="text" class="col-xs-12 type_select" ' +
    'id="%s" name="%s" readonly=true>', id, id);
    in_content += '<div class="zTreeDemoBackground left">';
    in_content += $.parseStr('<ul id="%s" style="height:200px;border:1px ' +
    'dashed #B9C0C5;"class="ztree asset_type_tree"></ul>', ulId);
    in_content += '</div>';
    return in_content;
}

function initDom() {
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
            onClick: getSelectLtreeNode1
        }
    };

    loadTypeList("asset_type_tree", 0);
    loadTypeList("asset_type_tree_c", 2);
}


/*
 * 加载树
 */
function loadTypeList(id, num) {
    $.ajax({
        type: 'POST',
        url: '/stock_in/asset/types',
        dataType: "json",
        data: {return_val: num},
        success: function (resp) {
            $.fn.zTree.init($("#" + id), setting, resp);
            window.zTree = $.fn.zTree.getZTreeObj(id);
            zTree.expandNode(zTree.getNodeByParam('pId', 0));
        }
    });
}

/*
 * ztree获取点击的节点值
 */
//{
// 得到完整的节点路径
function getNodePath(node) {
    /*
     *  根据节点数据的属性搜索
     *  getNodeByParam(key, value, parentNone)
     *  返回值：匹配精确搜索的节点数据
     *  @parm:key   ： 需要精确匹配的搜索名称
     *  @parm:value ：需要精确匹配的属性值，可以是任何类型，
     *                只要保证与 key 指定的属性值保持一致即可
     *  @parm:parentNone : 搜索范围，指定在某个父节点下的子节点中进行搜索
     *  返回值：如无结果，返回 null
     */
    if (!node) {
        return "";
    }
    var appName = node.name;
    var pId = node.pId;
    //树的深度上限是15
    for (var i = 0; i < 15; i++) {
        var pNode = window.zTree.getNodeByParam('id', pId);
        if (pNode) {
            appName = pNode.name + '.' + appName;
            pId = pNode.pId;
        } else {
            break;
        }
    }
    return appName;
}

function getSelectLtreeNode1(event, treeId, treeNode) {
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

        $("#asset_type").val(assetTypeVal);
        // 使其自定义校验生效
        $("#stock_new_in").find("form").validate().element($("#asset_type"));

        if (!arrNodes) {
            //说明：当选择没有父节点时，才将得到的值加进input中
            /*
             * 每次选择资产类别时，每点击一个节点，就将对应的品牌select框清除再创建
             * 防止品牌累加
             */
        }

//      ================这里是新增入库
        postSelectValue('provider', '/asset_info/prov/types', assetTypeVal, '请选择品牌');
        var list = getActualEnChList(assetTypeVal);
        var enlist = list[0];
        var chlist = list[1];
        var asset_content = constructActualAdd('abc', chlist, enlist, 2, 0);
        $("#other").empty();
        $("#other").append(asset_content);
        $("#other").show();
        $("#button").append($("#operate").show());
        $('#other').find("textarea[name='remark']").val('新增库存');
        $('#other').find("input[name='userful_life']").on('click', function () {
            WdatePicker({dateFmt: 'yyyy-MM-dd'});
        });
        $('#provider').change(function () {
            var proVal = $('#provider').val();
            postSelectValue('model', '/asset_info/model/types', assetTypeVal + '_' + proVal, '请选择型号');
        });
        getSelectInValue('device_state', '/asset_info/loadstate/1', '可用');
        getSelectValue('store_place', '/asset_info/loadstate/3', '请选择存放地点');
        getSelectValue('in_out_reason', '/asset_info/loadstate/4', '采购入库');
        if (containsValue(consumeList(), assetTypeVal)) {
            $('#store_place').change(function () {
                if ($('#store_place').val().substr(0, 1) != "请") {
                    constructPostParams();
                }
            });
        }

        $('#store_place').change(function () {
            if ($('#store_place').val().substr(0, 1) != "请") {
                getAdminNameByStorePlace($('#store_place').val(), 'other', 'user_name');
            }
        });

        autoShowInfo('other', 'user_name');
//      ================这里是新增入库结束

//      ================这里是耗材回收入库
        $("#asset_type_c").val(assetTypeVal);
        postSelectValue('provider_c', '/asset_info/prov/types', assetTypeVal, '请选择品牌');
        $('#provider_c').change(function () {
            var proVal = $('#provider_c').val();
            postSelectValue('model_c', '/asset_info/model/types', assetTypeVal + '_' + proVal, '请选择型号');
            autoShowInfo('stock_consume_device', 'user_name_c');
        });

    }
}

function showUseNum() {
    var user_name = $("#stock_consume_device").find("input[name='user_name_c']").val();
    if (!isNull(user_name)) {
        var list = ["asset_type", "provider", "model", "user_name"];
        var params = {};
        for (var i = 0; i < 4; i++) {
            params[list[i]] = $("#" + list[i] + "_c").val();
        }
        $.ajax({
            "dataType": 'json',
            "type": "POST",
            "url": "consume/use_num",
            'data': params,
            "success": function (resp) {
                console.log(resp);
                if ('user_name' in resp) {//有数据
                    $("#stock_consume_device").find("input[name='in_num_c']").val(resp['in_num']);
                    $('#stock_consume_device').find("input[name='user_name_c']").attr("readonly", "true");
                    $('#stock_consume_device').find("input[name='in_num_c']").attr("readonly", "true");
                } else {
                    $("#stock_consume_device").find("input[name='in_num_c']").val("0");
                    $('#stock_consume_device').find("input[name='in_num_c']").attr("readonly", "true");
                }

            },
            error: function (resp) {
                showErrorTips();
            }
        });
    }

}

function constructPostParams() {
    var list = ["asset_type", "provider", "model", "store_place"];
    var params = {};
    for (var i = 0; i < 4; i++) {
        params[list[i]] = $("#" + list[i]).val();
    }
    getSelectValNum("consume/num", params);
}


function getSelectValNum(url, params) {
    //  下拉框值从数据库选择,并且设置默认值
    $.ajax({
        "dataType": 'json',
        "type": "POST",
        "url": url,
        'data': params,
        "success": function (resp) {
            if ('user_name' in resp) {//有数据
                $("#other").find("input[name='user_name']").val(resp['user_name']);
                $("#other").find("input[name='in_num1']").val(resp['in_num1']);
                $('#other').find("input[name='user_name']").attr("readonly", "true");
                $('#other').find("input[name='in_num1']").attr("readonly", "true");
            } else {
                $("#other").find("input[name='in_num1']").val("0");
                $('#other').find("input[name='in_num1']").attr("readonly", "true");
            }

        },
        error: function (resp) {
            showErrorTips();
        }
    });
}

function initQueryDom(num) {
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
            onClick: getSelectLtreeNode2
        }
    };

    loadTypeList("asset_type_tree", num);

}


function getSelectLtreeNode2(event, treeId, treeNode) {
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

        $("#s_asset_type").val(assetTypeVal);
        // 使其自定义校验生效
        if (!arrNodes) {
            //说明：当选择没有父节点时，才将得到的值加进input中
            /*
             * 每次选择资产类别时，每点击一个节点，就将对应的品牌select框清除再创建
             * 防止品牌累加
             */
        }
        postSelectValue('s_provider', '/asset_info/prov/types', assetTypeVal, '请选择品牌');
        $('#s_provider').change(function () {
            var proVal = $('#s_provider').val();
            postSelectValue('s_model', '/asset_info/model/types', assetTypeVal + '_' + proVal, '请选择型号');
        });
    }
}


function initConsumeInDom() {
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
            onClick: getSelectLtreeNode3
        }
    };
    loadTypeList('in_asset_type_tree');
}
function getSelectLtreeNode3(event, treeId, treeNode) {
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

        $("#in_asset_type").val(assetTypeVal);
        // 使其自定义校验生效
        if (!arrNodes) {
            //说明：当选择没有父节点时，才将得到的值加进input中
            /*
             * 每次选择资产类别时，每点击一个节点，就将对应的品牌select框清除再创建
             * 防止品牌累加
             */
        }
        postSelectValue('in_provider', '/asset_info/prov/types', assetTypeVal, '请选择品牌');
        $('#in_provider').change(function () {
            var proVal = $('#in_provider').val();
            postSelectValue('in_model', '/asset_info/model/types', assetTypeVal + '_' + proVal, '请选择型号');
        });
    }
}

function initConsumeOutDom() {
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
            onClick: getSelectLtreeNode4
        }
    };
    loadTypeList('out_asset_type_tree');
}
function getSelectLtreeNode4(event, treeId, treeNode) {
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
        $("#out_asset_type").val(assetTypeVal);
        // 使其自定义校验生效
        if (!arrNodes) {
            //说明：当选择没有父节点时，才将得到的值加进input中
            /*
             * 每次选择资产类别时，每点击一个节点，就将对应的品牌select框清除再创建
             * 防止品牌累加
             */
        }
        postSelectValue('out_provider', '/asset_info/prov/types', assetTypeVal, '请选择品牌');
        $('#out_provider').change(function () {
            var proVal = $('#out_provider').val();
            postSelectValue('out_model', '/asset_info/model/types', assetTypeVal + '_' + proVal, '请选择型号');
        });
    }
}