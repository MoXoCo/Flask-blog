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

