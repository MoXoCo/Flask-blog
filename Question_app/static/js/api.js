/**
 * Created by gua on 7/11/16 4:28:01
 */

// log
var log = function () {
    console.log(arguments);
};

// form
var formFromKeys = function(keys, prefix) {
    var form = {};
    for(var i = 0; i < keys.length; i++) {
        var key = keys[i];
        var tagid = prefix + key;
        var value = $('#' + tagid).val();
        if (value.length < 1) {
            // alert('字段不能为空');
            break;
        }
        form[key] = value;
    }
    return form;
};

// vip API
var vip = {
  data:{}
};

vip.ajax = function(url, method, form, success, error) {
    var request = {
        url: url,
        type: method,
        contentType: 'application/json',
        success: function (r) {
            log('vip post success', url, typeof r, r);
            success(r);
        },
        error: function (err) {
            r = {
                success: false,
                data: err
            }
            log('vip post err', url, err);
            error(r);
        }
    };
    if(method === 'post') {
        var data = JSON.stringify(form);
        request.data = data;
    }
    $.ajax(request);
};

vip.get = function(url, response) {
    var method = 'get';
    var form = {}
    this.ajax(url, method, form, response, response);
};

vip.post = function(url, form, success, error) {
    var method = 'post';
    this.ajax(url, method, form, success, error);
};

// API normal
//vip.register = function(form, success, error) {
//    var url = '/register';
//    this.post(url, form, success, error);
//};
//
//vip.login = function(form, success, error) {
//    var url = '/login';
//    this.post(url, form, success, error);
//};

// tweet API
vip.commentAdd = function(form, success, error) {
    var url = '/comment/edit/' + form.post_id;
    this.post(url, form, success, error);
};
