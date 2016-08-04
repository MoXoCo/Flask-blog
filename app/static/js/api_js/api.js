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
var vip = {};

vip.ajax = function(url, method, form, response) {
    var request = {
        url: url,
        type: method,
        contentType: 'application/json',
        success: function (r) {
            log('vip post success', url, r);
            response(r);
        },
        error: function (err) {
            r = {
                success: false,
                message: '我们自行生成的网络错误',
                data: err
            }
            log('vip post err', url, err);
            response(r);
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
    this.ajax(url, method, form, response);
};

vip.post = function(url, form, response) {
    var method = 'post';
    this.ajax(url, method, form, response);
};

//auth api
vip.register = function(form, response) {
    var url = '/register';
    this.post(url, form, response);
};

vip.login = function(form, response) {
    var url = '/login';
    this.post(url, form, response);
};

//post api
vip.postAdd = function(form, response) {
    var url = '/api/post/add';
    this.post(url, form, response);
};

vip.postDelete = function(form, response) {
    var id = form.id;
    var url = '/api/post/delete/' + id;
    this.get(url, response);
};

// comment api
vip.commentAdd = function(form, response) {
    var id = $('.comment').attr('data-pid');
    var url = '/api/comment/add/' + id;
    this.post(url, form, response);
};

vip.commentDelete = function(form, response) {
    var id = form.id;
    var url = '/api/comment/delete/' + id;
    this.get(url, response);
};

// follow api
vip.userFollow = function(form, response) {
    var url = '/api/follow/' + form.name;
    this.get(url, response);
};

vip.userUnFollow = function(form, response) {
    var url = '/api/unfollow/' + form.name;
    this.get(url, response);
};

// at api
vip.atPostInsert = function(form, response) {
    var url = '/api/at/user/' + form.name;
    this.get(url, response);
};

