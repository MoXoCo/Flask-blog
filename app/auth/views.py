from . import auth
from flask import render_template
from flask import url_for
from flask import redirect
from flask import session
from flask import request
from flask import jsonify
from flask import abort

from ..models import User
from ..models import ResponseData as response
from ..mylog import log
from ..main.views import required_login
from ..main.views import current_user

@auth.route('/login')
def login_view():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login():
    form = request.get_json()
    username = form.get('username', '')
    user = User.query.filter_by(username=username).first()
    if user is not None and user.validate_auth(form):
        next = url_for('main.index')
        msgs= '登录成功'
        r = response(msgs).success(next)
        #log('r, ',r)
        #session.permanent = True
        session['username'] = username
    else:
        msgs = '登录失败'
        r = response(msgs=msgs).error()
    return jsonify(r)

@auth.route('/logout')
@required_login
def logout():
    u = current_user()
    session.pop('username')
    log('{}已经注销了!'.format(u))
    return redirect(url_for('.login_view'))


@auth.route('/register', methods=['POST'])
def register():
    form = request.get_json()
    u = User(form)
    status, msgs = u.valid()
    if status:
        u.save()
        #session.permanet = True
        session['username'] = u.username
        next = url_for('.login_view')
        r = response().success(next)
    else:
        message = '\n'.join(msgs)
        r = response(msgs=message).error()
    return jsonify(r)


@auth.route('/rename')
@required_login
def rename_view():
    return render_template('rename.html', user=current_user())


@auth.route('/rename', methods=['POST'])
@required_login
def rename():
    user = current_user()
    username = request.form.get('username')
    if User.query.filter_by(username=username).first() is None:
        user.username = username
        user.save()
        return redirect(url_for('.login_view'))
    else:
        abort(404)


@auth.route('/repassword')
@required_login
def repassword_view():
    return render_template('repassword.html', user=current_user())


@auth.route('/repassword', methods=['POST'])
@required_login
def repassword():
    user = current_user()
    password = request.form['password']
    log('debug repassword: ', password)
    user.password = password
    user.save()
    return redirect(url_for('.login_view'))