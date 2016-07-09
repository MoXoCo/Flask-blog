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
        log('value: ',value)
        if (value.length < 1) {
            // alert('字段不能为空');
            break;
        }
        form[key] = value;
    }
    return form;
};

// weibo API
var weibo = {};

weibo.delete = function(url) {
    var self = $(this);
    var id = $('.id-button-delete').attr('data-id');
    log('id: ', id)
    var request = {
        url: url + '/' + id,
        type: 'get',
        success: function(r) {
            log('get success: ', url, r);
            if(r.success){
                log('删除成功： ',id, r)
                self.parent().remove();
            }
        }
    };
    $.ajax(request);
};

weibo.post = function(url, form, success, error) {
    var data = JSON.stringify(form);
    var request = {
        url: url,
        type: 'post',
        contentType: 'application/json',
        data: data,
        success: function (r) {
            //log('post success', url, r);
            log('post success', url, r);
            success(r);
        },
        error: function (err) {
            log('post err', url, err);
            error(err);
        }
    };
    $.ajax(request);
};

weibo.register = function(form, success, error) {
    var url = '/register';
    this.post(url, form, success, error);
};

weibo.login = function(form, success, error) {
    var url = '/login';
    this.post(url, form, success, error);
};

weibo.editPost = function(form, success, error) {
    var url = '/post/edit';
    this.post(url, form, success, error);
};

weibo.editComment = function(form, success, error) {
    var post_id = $('#id-div-add').attr('data-id');
    log('post_id',post_id);
    var url = '/comment/edit/' + post_id;
    this.post(url, form, success, error);
};

weibo.deletePost = function() {
    var url = '/post/delete';
    this.delete(url);
};