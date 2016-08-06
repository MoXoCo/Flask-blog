from flask import render_template
from flask import session
from flask import Blueprint
from flask import request

from ..models import User
from ..models import Post
from ..models import Comment

main = Blueprint('main', __name__)

def current_user():
    username = session.get('username', '')
    u = User.user_by_name(username)
    return u

@main.route('/')
def index():
    posts = Post.query.filter_by(is_delete=False).\
        order_by(Post.timestamp.desc()).all()
    u = current_user()
    return render_template('index.html', posts=posts, u=u)


@main.route('/post/<post_id>')
def post_view(post_id):
    post = Post.query.get_or_404(post_id)
    u = current_user()
    return render_template('post.html', post=post, u=u)

@main.route('/user/<username>')
def user(username):
    u = current_user()
    user = User.user_by_name(username)
    posts = user.posts.filter(
        Post.is_delete==False
    ).order_by(
        Post.timestamp.desc()).all()
    args = dict(
        u=u,
        user=user,
        posts=posts,
    )
    return render_template('user.html', **args)


@main.route('/test')
def test():
    u = current_user()
    return render_template('form.html', u=u)






