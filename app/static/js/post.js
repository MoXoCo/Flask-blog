var editPostForm = function () {
    var keys = [
        'post',
    ];
    var editPostPrefix = 'id-textarea-';
    var form = formFromKeys(keys, editPostPrefix);
    return form;
};

var editPost = function () {
    var form = editPostForm();
    var success = function (r) {
        log('edit post: ', r);
        if (r.success) {
            log('服务器返回了： ',typeof r, r);
            log('成功添加微博！');
            $('#id-template-post').tmpl(r.data).insertAfter('#id-h1-add')
            $('#id-textarea-post').val('')
        }
    };
    var error = function (err) {
        log('edit post: ', err);
        alert(err)
    }
    weibo.editPost(form, success, error);
};

var deletePost = function (id, self) {
    weibo.deletePost(id, self);
};

