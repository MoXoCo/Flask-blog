from ..models import User
from ..models import At
from . import api
from . import api_response
from ..HelpFunc import log
from flask import jsonify
from flask import request
from flask import url_for

@api.route('/at/user/<username>')
def user_ated(username):
    user = User.user_by_name(username)
    at_list = user.ats.filter_by(is_readed=False).order_by(At.timestamp.desc()).all()
    if len(at_list) == 0:
        at_list = user.ats.filter_by(is_delete=False).order_by(At.timestamp.desc()).all()
    data = []
    for at in at_list:
        at.is_readed = True
        at.save()
        data.append(at.json())
    print('data : ', data)
    r = api_response().success(data)
    return jsonify(r)


@api.route('/personal/msg/<username>', methods=['POST'])
def write_personal_msg(username):
    user = User.user_by_name(username)
    form = request.get_json()
    log('form: ', form)
    user.save_personal_msg(form)
    next = url_for('main.user', username=username)
    r = api_response().success(next=next)
    return jsonify(r)


@api.route('/personal/msg/<username>')
def personal_msg(username):
    user = User.user_by_name(username)
    data = user.personal_msg()
    r = api_response().success(data=data)
    return jsonify(r)


