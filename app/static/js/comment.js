var editCommentForm = function () {
    var keys = [
        'comment',
    ];
    var editPostPrefix = 'id-textarea-';
    var form = formFromKeys(keys, editPostPrefix);
    return form;
};

// actions
var editComment = function () {
    var form = editCommentForm();
    var success = function (r) {
        log('edit comment: ', r);
        if (r.success) {
            log('服务器返回了： ',typeof r, r);
            log('成功添加评论！');
            $('#id-template-comment').tmpl(r.data).insertBefore('#id-div-add')
            $('#id-textarea-comment').val('')
        }
    };
    var error = function (err) {
        log('edit comment: ', err);
        alert(err)
    }
   weibo.editComment(form, success, error);
};


var deleteComment = function (id, self) {
    weibo.deleteComment(id, self);
};