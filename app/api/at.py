from ..models import User
from ..models import At
from . import api
from . import api_response
from flask import jsonify

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