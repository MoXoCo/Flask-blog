from ..models import User
from flask import jsonify
from flask import session
from flask import Blueprint

from functools import wraps

api = Blueprint('api', __name__)


def current_user():
    username = session.get('username', '')
    u = User.query.filter_by(username=username).first()
    return u


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            r = {
                'success': False,
                'message': '未登录',
            }
            return jsonify(r)
        return f(*args, **kwargs)
    return function


class api_response(object):
    @staticmethod
    def success(data=None, message=None, next=None):
        d = dict(
            success=True,
            data=data,
            message=message,
            next=next
        )
        return d

    @staticmethod
    def error(message):
        d = dict(
            success=False,
            message=message,
        )
        return d

from . import post
from . import comment
from . import follow
from . import at_and_user

