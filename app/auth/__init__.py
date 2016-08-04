from flask import request
from flask import url_for
from flask import render_template
from flask import jsonify
from flask import session
from flask import Blueprint
from ..api import api_response
from ..models import Post

from ..models import User
from functools import wraps

auth = Blueprint('auth', __name__)

def current_user():
    username = session.get('username', '')
    u = User.query.filter_by(username=username).first()
    return u


@auth.route('/login')
def login_view():
    return render_template('login.html')


# 处理注册的请求  POST
@auth.route('/register', methods=['POST'])
def register():
    print('register')
    form = request.get_json()
    u = User(form)
    status, msgs = u.register_validate()
    if status:
        print("register success", form)
        u.save()
        next = request.args.get('next', url_for('main.index'))
        r = api_response().success(next=next)
        session['username'] = u.username
    else:
        print('register failed', form)
        message = '\n'.join(msgs)
        r = api_response().error(message=message)
    return jsonify(r)


# 处理登录请求  POST
@auth.route('/login', methods=['POST'])
def login():
    form = request.get_json()
    username = form.get('username', '')
    user = User.user_by_name(username)

    print('user login', user, form)
    if user is not None and user.validate_auth(form):
        next= request.args.get('next', url_for('main.index'))
        r = api_response().success(next=next)
        session['username'] = username
    else:
        msg = '登录失败'
        r = api_response().error(message=msg)
    return jsonify(r)
