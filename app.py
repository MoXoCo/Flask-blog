from flask import render_template
from flask import redirect
from flask import abort
from flask import url_for
from flask import session
from flask import request
from flask import flash

from models import app
from models import User
from models import Post
from models import Comment
from models import At
from models import AnonymousUser

from mylog import log
from functools import wraps
import re


def current_user():
    try:
        user_id = session['user_id']
        u = User.query.filter_by(id=user_id).first()
    except KeyError:
        u = AnonymousUser()
    return u

def at_users(content):
    pattern = re.compile(r'@(\w+)\s')
    users = pattern.findall(content)
    log('at users: ', users)
    return users



def required_login(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user.is_user():
            return redirect(url_for('login_view'))
        else:
            return f(*args, **kwargs)
    return wrapper


@app.route('/')
@required_login
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html',
                           posts=posts,
                           user=current_user())


@app.route('/login')
def login_view():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    u = User(request.form)
    user = User.query.filter_by(username=u.username).first()
    if u.validate(user):
        flash('登陆成功！')
        log('{}登陆成功！'.format(user))
        session['user_id'] = user.id
        return redirect(url_for('index'))
    else:
        flash('登陆失败！')
        log('登陆失败！')
        return redirect(url_for('login_view'))

@app.route('/logout')
@required_login
def logout():
    u = current_user()
    session.pop('user_id')
    flash('你已经注销了！')
    log('{}已经注销了!'.format(u))
    return redirect(url_for('login_view'))


'''
@app.route('/register')
def register_view():
    return render_template('register.html')
'''

@app.route('/register', methods=['POST'])
def register():
    u = User(request.form)
    user = User.query.filter_by(username=u.username).first()
    if u.valid() and user is None:
        log('{}注册成功！'.format(u))
        u.save()
        u.follow(u.id)
        return redirect(url_for('login_view'))
    else:
        flash('注册失败！')
        log('注册失败！')
        return redirect(url_for('login_view'))


@app.route('/user/<username>')
@required_login
def user(username):
    u = User.query.filter_by(username=username).first()
    user = current_user()
    if u != user:
        u.increase_visitors()
    posts = u.posts.order_by(Post.timestamp.desc()).all()
    ated_num = u.ats.filter_by(is_readed=False).count()
    log('debug ated_num: ', ated_num)
    kwargs = {
        'posts': posts,
        'u': u,
        'user': user,
        'ated_num': ated_num
    }
    return render_template('user.html', **kwargs)

@app.route('/post/<post_id>')
@required_login
def post_view(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',
                           post=post,
                           user=current_user())


@app.route('/post/edit', methods=['POST'])
@required_login
def post_edit():
    form = request.form
    content = form.get('content', None)
    if len(content) == 0:
        return redirect(url_for('index'))
    post = Post(form)
    post.user = current_user()
    post.save()
    if '@' in content:
        users = at_users(content)
        for u in users:
            at = At()
            at.user = User.query.filter_by(username=u).first()
            at.post = post
            at.save()
    flash('文章已发表！')
    log('文章已发表！')
    return redirect(url_for('index'))


@app.route('/post/update/<post_id>')
@required_login
def post_update_view(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return abort(404)
    return render_template('post_update.html', post=post)


@app.route('/post/update/<post_id>', methods=['POST'])
@required_login
def post_update(post_id):
    post = Post.query.filter_by(id=post_id).first()
    user = current_user()
    form = request.form
    content = form.get('content', None)
    if len(content) == 0:
        return redirect(url_for('index'))

    if user.id == post.user.id or user.is_admin():
        post.content = content
        post.save()
        log('文章修改成功！')
        return redirect(url_for('index'))
    else:
        abort(401)


@app.route('/post/delete/<post_id>')
@required_login
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    user = current_user()
    if user.id == post.user.id or user.is_admin():
        post.is_delete = True
        post.save()
        flash('文章已删除！')
        log('文章已删除！')
        return redirect(url_for('index'))
    else:
        abort(401)


@app.route('/comment/edit/<post_id>', methods=['POST'])
def comment_edit(post_id):
    post = Post.query.filter_by(id=post_id).first()
    user = current_user()
    form = request.form
    content = form.get('content', None)
    if len(content) == 0:
        return redirect(url_for('post_view', post_id=post_id))
    c = Comment(form)
    c.post = post
    c.user = user
    c.save()
    if '@' in content:
        users = at_users(content)
        for u in users:
            at = At()
            at.user = User.query.filter_by(username=u).first()
            at.comment = c
            at.post = post
            at.save()
    log('评论发表成功！')
    flash('评论发表成功！')
    return redirect(url_for('post_view', post_id=post_id))


@app.route('/comment/update/<comment_id>')
@required_login
def comment_update_view(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return render_template('comment_update.html', comment=comment)


@app.route('/comment/update/<comment_id>', methods=['POST'])
@required_login
def comment_update(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    user = current_user()
    content = request.form.get('content', None)
    if len(content) == 0:
        return redirect(url_for('post_view', post_id=comment.post_id))
    else:
        if user.id == comment.user_id or user.is_admin():
            comment.content = content
            comment.save()
            flash('评论发表成功！')
            log('评论发表成功！')
            return redirect(url_for('post_view', post_id=comment.post_id))
        else:
            abort(401)


@app.route('/comment/delete/<comment_id>')
@required_login
def comment_delete(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    user = current_user()
    if user.id == comment.user_id or user.is_admin():
        comment.is_delete = True
        comment.save()
        return redirect(url_for('post_view', post_id=comment.post_id))
    else:
        abort(401)


@app.route('/comment/reply/<comment_id>')
@required_login
def commment_reply_view(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return render_template('comment_reply.html', comment=comment)


@app.route('/comment/reply/<comment_id>', methods=['POST'])
@required_login
def commment_reply(comment_id):
    form = request.form
    comment = Comment.query.get_or_404(comment_id)
    content = form.get('content', None)
    if len(content) == 0:
        return redirect(url_for('post_view', post_id=comment.post_id))
    else:
        c = Comment(form)
        c.post = comment.post
        c.user = current_user()
        c.previous_comment_id = comment.id
        c.save()
        return redirect(url_for('post_view', post_id=comment.post_id))


@app.route('/follow/<user_id>')
@required_login
def follow(user_id):
    u = User.query.get_or_404(user_id)
    user = current_user()
    if not user.is_following(user_id):
        user.follow(user_id)
        log('{}关注{}成功！'.format(user, u))
        flash('关注用户成功!')
        return redirect(url_for('user', username=u.username))


@app.route('/unfollow/<user_id>')
@required_login
def unfollow(user_id):
    u = User.query.get_or_404(user_id)
    user = current_user()
    if user.is_following(user_id):
        user.follow(user_id)
        log('{}取消对{}关注！'.format(user, u))
        flash('已取消对用户的关注!')
        return redirect(url_for('user', username=u.username))


@app.route('/at/user/<user_id>')
def user_ated_view(user_id):
    u = User.query.get_or_404(user_id)
    ats = u.ats.order_by(At.timestamp.desc()).all()
    posts = []
    for at in ats:
        at.is_readed = True
        at.save()
        posts.append(Post.query.filter_by(id=at.post_id).first())
    return render_template('user_ated.html', posts=posts)


@app.route('/rename')
@required_login
def rename_view():
    return render_template('rename.html', user=current_user())


@app.route('/rename', methods=['POST'])
@required_login
def rename():
    user = current_user()
    username = request.form.get('username')
    if User.query.filter_by(username=username).first() is None:
        user.username = username
        user.save()
        return redirect(url_for('login_view'))
    else:
        abort(404)


@app.route('/repassword')
@required_login
def repassword_view():
    return render_template('repassword.html', user=current_user())


@app.route('/repassword', methods=['POST'])
@required_login
def repassword():
    user = current_user()
    password = request.form['password']
    log('debug repassword: ', password)
    user.password = password
    user.save()
    return redirect(url_for('login_view'))


if __name__ == '__main__':
    '''
    args = {
        'port': 11000,
        'debug': True,
        'host': '0.0.0.0',
    }
    '''
    app.run(debug=True)
