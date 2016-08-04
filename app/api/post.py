from ..models import User
from ..models import Post
from ..models import At
from ..HelpFunc import log
from . import api
from . import current_user
from . import api_response

from flask import request
from flask import jsonify
import re


def username_ated(content):
    pattern = re.compile(r'@(\w+)\s')
    name_list = pattern.findall(content)
    return name_list

@api.route('/post/add', methods=['POST'])
def post_add():
    u = current_user()
    form = request.get_json()
    p = Post(form)
    p.user_id = u.id
    p.save()
    data = p.json()
    r = api_response().success(data=data)

    # 检查是否有用户被at
    content = form.get('post', '')
    if '@' in content:
        users_name = username_ated(content)
        for username in users_name:
            user = User.user_by_name(username)
            at = At(user.id, p.id)
            at.save()
    return jsonify(r)


@api.route('/post/delete/<post_id>')
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    user = current_user()
    if user.id == post.user.id or user.is_admin():
        post.is_delete = True
        post.save()
        for at in post.ats.all():
            at.delete()
        log('文章已删除！')
        r = api_response.success()
        return jsonify(r)
    else:
        msg = '删除失败'
        r = api_response.error(msg)
        return jsonify(r)

