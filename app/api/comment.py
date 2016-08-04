from ..models import User
from ..models import Comment
from ..models import At
from ..HelpFunc import log
from . import api
from . import current_user
from . import api_response
from .post import username_ated

from flask import request
from flask import jsonify

@api.route('/comment/add/<post_id>', methods=['POST'])
def comment_add(post_id):
    u = current_user()
    form = request.get_json()
    c = Comment(form)
    c.user_id = u.id
    c.post_id = post_id
    c.save()
    data = c.json()
    r = api_response().success(data=data)

    # 检查是否有用户被at
    content = form.get('comment', '')
    if '@' in content:
        users_name = username_ated(content)
        for username in users_name:
            user = User.user_by_name(username)
            at = At(user.id, post_id, c.id)
            at.save()
    return jsonify(r)


@api.route('/comment/delete/<comment_id>')
def comment_delete(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    user = current_user()
    if user.id == comment.user.id or user.is_admin():
        comment.is_delete = True
        comment.save()
        log('文章已删除！')
        for at in comment.ats.all():
            at.delete()
        r = api_response.success()
        return jsonify(r)
    else:
        msg = '删除失败'
        r = api_response.error(msg)
        return jsonify(r)
