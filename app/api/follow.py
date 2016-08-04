from ..models import User
from ..HelpFunc import log
from . import api
from . import current_user
from . import api_response
from flask import jsonify


@api.route('/follow/<username>')
def follow(username):
    user = User.user_by_name(username)
    u = current_user()
    if not u.is_following(user.id):
        u.follow(user.id)
        r = api_response().success()
        return jsonify(r)


@api.route('/unfollow/<username>')
def unfollow(username):
    user = User.user_by_name(username)
    u = current_user()
    if u.is_following(user.id):
        u.unfollow(user.id)
        r = api_response().success()
        return jsonify(r)