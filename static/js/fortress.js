/**
 * Created by lei on 2019/4/3.
 */
/** 侧栏菜单 **/
function activeNav() {
    var url_array = document.location.pathname.split("/");
    var app = url_array[1];
    var resource = url_array[2];
    //console.log(app);
    console.log(resource);
    if (app === ''){
        $('#index').addClass('active');
        $('#index').parent().parent().parent().addClass('menu-open');
    } else if (resource === ''){
        $("#" + app).addClass('active');
        $("#" + app).parent().addClass('menu-open');
    } else  {

        $("#" + app).addClass('active');
        $("#" + app).parent().addClass('menu-open');
        $('#' + resource).addClass('active');
    }
}

/**
 * Created by lei on 2018/10/23.
 */
/** 初始化 datatable **/
var cmdb = {};

cmdb.initDataTable = function(options){
    var ele = options.ele || $('.dataTable');
    var columnDefs = [
      {
          targets: 0,
          orderable: false,
          createdCell: function (td, cellData) {
              $(td).html('<input type="checkbox" class="text-center ipt_check" id=99991937>'.replace('99991937', cellData));
          }
      },
      {className: 'text-center', targets: '_all'}
    ];
    columnDefs = options.columnDefs ? options.columnDefs.concat(columnDefs) : columnDefs;
    var table = ele.DataTable({
        columns: options.columns || [],
        //order: options.order || [],
        language: {
            search: "搜索",
            lengthMenu: "每页  _MENU_",
            info: "显示第 _START_ 至 _END_ 项结果; 总共 _TOTAL_ 项",
            infoFiltered:   "",
            infoEmpty:      "",
            zeroRecords:    "没有匹配项",
            emptyTable:     "没有记录",
            paginate: {
                first:      "首页",
                previous:   "上一页",
                next:       "下一页",
                last:       "尾页"
            }
        }
    });
    return table;
};

cmdb.initServerDataTable = function (options) {
    var ele = options.ele || $(".dataTable");
    var columnDefs = [
        {
            targets: 0,
            orderable: false,
            createdCell: function (td, cellData) {
                $(td).html('<input type="checkbox" class="text-center ipt_check" data-uid=99991937>'.replace('99991937', cellData));
            }
        },
        {className: 'text-center', targets: '_all'}
    ];
    columnDefs = options.columnDefs ? options.columnDefs.concat(columnDefs) : columnDefs;
      var select = {
            style: 'multi',
            selector: 'td:first-child'
      };
    var table = ele.DataTable({
        language: {
            search: "搜索",
            lengthMenu: "每页  _MENU_",
            info: "显示第 _START_ 至 _END_ 项结果; 总共 _TOTAL_ 项",
            infoFiltered:   "",
            infoEmpty:      "",
            zeroRecords:    "没有匹配项",
            emptyTable:     "没有记录",
            paginate: {
                first:      "首页",
                previous:   "上一页",
                next:       "下一页",
                last:       "尾页"
            }
        },
        ajax: {
            url: options.ajax_url,
            dataType: 'json',
            type: 'POST',
//            data: {filter:JSON.stringify(options.columns)},
            headers:{'Content-Type': "application/x-www-form-urlencoded"},
            //data: function(data){
            //    console.log(data);
            //}
        },
        select: options.select || select,
        serverSide: true,
        processing: false,
        deferRender: true,
        pageLength: options.pageLength || 15,
        order: options.order || [],
        columnDefs: columnDefs,
        columns: options.columns || [],

        //"aoColumnDefs": [{
        //    "orderable": false,// 指定列不参与排序
        //    "aTargets": [0,7,9] // 指定 下标为[1,3,4,5,6]的不排序
        //}],
        lengthMenu: [[10, 15, 25, 50, -1], [10, 15, 25, 50, "All"]]
    });

    var table_id = table.settings()[0].sTableId;
    $('#' + table_id + ' .ipt_check_all').on('click', function() {
        if ($(this).prop("checked")) {
            $(this).closest('table').find('.ipt_check').prop('checked', true);
            //table.rows({search:'applied', page:'current'}).select();
        } else {
            $(this).closest('table').find('.ipt_check').prop('checked', false);
            //table.rows({search:'applied', page:'current'}).deselect();
        }
    });

    return table;
};

function APIUpdateAttr(props) {
    // props = {url: .., body: , success: , error: , method: ,}
    props = props || {};
    var success_message = props.success_message || '更新成功!';
    var fail_message = props.fail_message || '更新时发生未知错误.';
    var flash_message = props.flash_message || true;
    if (props.flash_message === false){
        flash_message = false;
    }
    console.log(props);
    $.ajax({
        url: props.url,
        type: props.method || "PATCH",
        data: props.data,
        //contentType: props.content_type || "application/json; charset=utf-8",
        dataType: props.data_type || "json"
    }).done(function(data, textStatue, jqXHR) {
        if (flash_message) {
            //console.log('step 1');
            //console.log(data);
            toastr.success(success_message);
        }
        if (typeof props.success === 'function') {
            //console.log('step 2');
            //console.log(data);
            return props.success(data);
        }

        if (props.data_table){
            //console.log('step 3');
            props.data_table.ajax.reload();
        }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        if (flash_message) {
            toastr.error(fail_message);
        }
        if (typeof props.error === 'function') {
            return props.error(jqXHR.responseText);
        }
    });
  // return true;
}



function objectActiveChange(obj,name,url,data_table,redirectTo){
    function doChange(){
        var body = {};
        var fail = function(){
            swal("错误","更新"+"[ "+name+" ]"+"遇到错误","error");
        };
        var success = function(){
            if (!redirectTo) {
                if(Array.isArray(obj)){
                    $.each(obj,function(i,j){
                        $(j).parent().parent().remove();
                    })
                }else {
                    $(obj).parent().parent().remove();
                }
            } else {
                setTimeout('window.location.reload()',2000);

            }
        };
        APIUpdateAttr({
            url: url,
            body: JSON.stringify(body),
            method: "GET",
            success_message: "更新成功",
            success: success,
            error: fail,
            data_table: data_table
        });
    }
    if(name.length == 0){
        swal({
            title: '没有选择项目!',
            text: "选项不能为空!",
            type: "error",
            confirmButtonText: '确认',
            closeOnConfirm: true
        },function(){
            return false;
        });
    }else {
        swal({
            title: '你确定修改状态吗 ?',
            text: " [" + name + "] ",
            type: "warning",
            showCancelButton: true,
            cancelButtonText: '取消',
            confirmButtonColor: "#ed5565",
            confirmButtonText: '确认',
            closeOnConfirm: true
        }, function () {
            doChange();
        });
    }

}

// Sweet Alert for Delete
function objectDelete(obj, name, url, redirectTo) {
    function doDelete() {
        var body = {};
        var success = function() {
            // swal('Deleted!', "[ "+name+"]"+" has been deleted ", "success");
            if (!redirectTo) {
                if(Array.isArray(obj)){
                    $.each(obj,function(i,j){
                        $(j).parent().parent().remove();
                    })
                }else {
                    $(obj).parent().parent().remove();
                }
            } else {
                window.location.href=redirectTo;
            }
        };
        var fail = function() {
            swal("错误", "删除"+"[ "+name+" ]"+"遇到错误", "error");
        };
        APIUpdateAttr({
            url: url,
            body: JSON.stringify(body),
            method: 'DELETE',
            success_message: "删除成功",
            success: success,
            error: fail
        });
    };
    //console.log(name.length);
    if(name.length == 0){
        swal({
            title: '没有选择项目!',
            text: "选项不能为空!",
            type: "error",
            confirmButtonText: '确认',
            closeOnConfirm: true
        },function(){
            return false;
        });
    }else {
        swal({
            title: '确定删除以下资产记录?',
            text: " [" + name + "] ",
            icon: "warning",
            buttons: true,
            dangerMode: true
        }).then(function(isConfirm) {
            if (!isConfirm) {
                swal('取消删除!', '主机信息未删除', 'error');

            } else {
                doDelete();
                swal('删除成功',{icon:'success'})
            }

        })
    };
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                // break;
            }
        }
    }
    return cookieValue;
}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function setAjaxCSRFToken() {
    var csrftoken = getCookie('csrftoken');
    var sessionid = getCookie('sessionid');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}
setAjaxCSRFToken();


/*
服务安装
 */

function softSwal(obj,options,data_table){
    options.name = obj.closest("tr").find(":nth-child(1)").children('label').html();
    options.version = obj.closest("tr").find(":nth-child(3)").html();
    var success = function() {
        swal('执行成功',options.name + ' : '+options.version+ ' 正在安装','success');
    };

    var fail = function() {
        swal("错误",options.name + ' : '+options.version+ ' 安装失败','error');
    };

    if(options.name.length == 0){
        swal({
            title: '没有选择项目!',
            text: "选项不能为空!",
            type: "error",
            confirmButtonText: '确认',
            closeOnConfirm: true
        },function(){
            return false;
        });
    }else {
        options.col.text = "服务名称:"+options.name+" 版本:"+options.version
        swal(options.col)
            .then(function(isConfirm){
                if(!isConfirm){
                    swal('取消安装','取消成功',"success")
                }else{
                    options.data = {
                        status:options.status,
                        soft_uid:obj.data('uid')
                    };
                    console.log(options.data);
                    APIUpdateAttr({
                        url: options.url,
                        data: options.data,
                        method: 'POST',
                        data_type:'json',
                        success_message: "更新成功",
                        success: success,
                        error: fail,
                        data_table:data_table
                    });
                }
            })
    }
}


/*
主机列表选择
 */

function assetSelect(sObj,dObj){
    var selected = $("#"+sObj+" option:selected");
    if(selected.length === 0){
        swal('没有选中主机','请先选择主机','error');
    }
    selected.clone().appendTo("#"+dObj);
    selected.remove();
}