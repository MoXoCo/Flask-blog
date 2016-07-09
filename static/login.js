var loginForm = function () {
    var keys = [
        'username',
        'password',
    ];
    var loginPrefix = 'id-input-login-';
    var form = formFromKeys(keys, loginPrefix);
    return form;
};

var registerForm = function () {
    var keys = [
        'username',
        'password',
    ];
    var registerPrefix = 'id-input-';
    var form = formFromKeys(keys, registerPrefix);
    return form;
};

var editPostForm = function () {
    var keys = [
        'post',
    ];
    var editPostPrefix = 'id-textarea-';
    var form = formFromKeys(keys, editPostPrefix);
    return form;
};

var editCommentForm = function () {
    var keys = [
        'comment',
    ];
    var editPostPrefix = 'id-textarea-';
    var form = formFromKeys(keys, editPostPrefix);
    return form;
};

// actions
var register = function () {
    var form = registerForm();
    var success = function (r) {
        log('reg, ', r);
        if (r.success) {
            log(r.next);
            window.location.href = r.next;
        } else {
            alert(r.message);
        }
    };
    var error = function (err) {
        log('reg, ', err);
    };
    // weibo 在 weibo.js 中
    // 在 index.html 中 weibo.js 先于 login.js 引入
    // 所以说这里可以直接用
    // 很野鸡吧?
    // 这就是 JavaScript
    weibo.register(form, success, error);
};

var login = function () {
    var form = loginForm();
    var success = function (r) {
        log('login, ', r);
        if (r.success) {
            log(r.next);
            // 登录成功后 用下面这句跳转
             window.location.href = r.next;
        } else {
            alert(r.message);
        }
    };
    var error = function (err) {
        log('login, ', err);
        alert(err);
    };
    weibo.login(form, success, error);
};

var editPost = function () {
    var form = editPostForm();
    var success = function (r) {
        log('edit post: ', r);
        if (r.success) {
            log('服务器返回了： ',typeof r, r);
            log('成功添加微博！');
            $('#id-template-post').tmpl(r.data).insertAfter('#id-h1-add')

        }
    };
    var error = function (err) {
        log('edit post: ', err);
        alert(err)
    }
    weibo.editPost(form, success, error);
};

var editComment = function () {
    var form = editCommentForm();
    var success = function (r) {
        log('edit comment: ', r);
        if (r.success) {
            log('服务器返回了： ',typeof r, r);
            log('成功添加评论！');
            $('#id-template-comment').tmpl(r.data).insertBefore('#id-div-add')
        }
    };
    var error = function (err) {
        log('edit comment: ', err);
        alert(err)
    }
   weibo.editComment(form, success, error);
};

var deletePost = function () {
    weibo.deletePost();
};