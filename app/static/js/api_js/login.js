var loginForm = function () {
    var keys = [
        'username',
        'password',
    ];
    var loginPrefix = 'id-input-login-';
    var form = formFromKeys(keys, loginPrefix);
    log('debug form: ', form)
    return form;
};

var registerForm = function () {
    var keys = [
        'username',
        'password',
    ];
    var registerPrefix = 'id-input-';
    var form = formFromKeys(keys, registerPrefix);
    log('debug form: ', form)
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
    // weibo 在 weibo.js 中
    // 在 index.html 中 weibo.js 先于 login.js 引入
    // 所以说这里可以直接用
    // 很野鸡吧?
    // 这就是 JavaScript
    vip.register(form, success);
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
    vip.login(form, success);
};

