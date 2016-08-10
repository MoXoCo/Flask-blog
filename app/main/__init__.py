from flask import render_template
from flask import session
from flask import Blueprint
from flask import request
from ..HelpFunc import log

from ..models import User
from ..models import Post
from ..models import Follow

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


@main.route('/<username>/followers')
def followers(username):
    u = current_user()
    user = User.user_by_name(username)
    followers = user.follower.order_by(Follow.timestamp.desc()).all()
    log('followers: ', followers)
    follows = [follow.follower for follow in followers if follow.follower_id != user.id]
    args = dict(
        u=u,
        user=user,
        follows=follows,
    )
    return render_template('follower.html', **args)


@main.route('/<username>/followees')
def followees(username):
    u = current_user()
    user = User.user_by_name(username)
    followees = user.followed.order_by(Follow.timestamp.desc()).all()
    log('followers: ', followees)
    follows = [follow.followed for follow in followees if follow.followed_id != user.id]
    args = dict(
        u=u,
        user=user,
        follows=follows,
    )
    return render_template('followed.html', **args)