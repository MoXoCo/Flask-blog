from flask import render_template
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify

import time
from mylog import log
from models import app
from models import Post
from models import Comment



@app.route('/')
def index_view():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.title.desc()).paginate(
        page, per_page=3, error_out=False
    )
    posts = pagination.items
    return render_template('index.html',
                           posts=posts,
                           pagination=pagination)


@app.route('/post/<post_id>')
def post_view(post_id):
    post = Post.query.get_or_404(post_id)
    pagination = Post.query.order_by(
        Post.title.desc()).filter(
        Post.title<=post.title).paginate(page=1, per_page=3)
    return render_template('post.html',
                           post=post,
                           pagination=pagination)


@app.route('/comment/edit/<post_id>', methods=['POST'])
def comment_edit(post_id):
    post = Post.query.get_or_404(post_id)
    form = request.get_json()
    log('d: ', form)
    content = form.get('comment', '')
    c = Comment(content)
    c.post = post
    c.save()
    log('评论发表成功')
    response = dict(
        success=True,
        data=c.json()
    )
    log('response: ', response)
    return jsonify(response)
    #return redirect(url_for('post_view', post_id=post_id))


@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)
    '''
    args = {
        'port': 11000,
        'debug': True,
        'host': '0.0.0.0',
    }
    app.run(**args)
    '''


