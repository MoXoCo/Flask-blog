from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import sql
from hashlib import sha1
from mylog import log
import random


db_path = 'db.sqlite'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///{}'.format(db_path)
app.secret_key = 'a random string'

db = SQLAlchemy(app)




class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=sql.func.now())

    def __repr__(self):
        return u'<User({}) follow User({})>'.format(
            self.follow_id, self.followed_id
        )

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password_hash= db.Column(db.String())
    timestamp = db.Column(db.DateTime(timezone=True),
                          default=sql.func.now())
    role = db.Column(db.Integer, default=2)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    ats = db.relationship('At', backref='user', lazy='dynamic')
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic')
    follower = db.relationship('Follow',
                               foreign_keys=[Follow.followed_id],
                               backref=db.backref('followed', lazy='joined'),
                               lazy='dynamic')


    def __init__(self, form):
        self.username = form.get('username', None)
        self.password = form.get('password', None)
        if self.username == 'admin':
            self.role = 1

    def __repr__(self):
        return u'<User {}>'.format(self.username)

    def _hashed_string(self, string):
        return sha1(string.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = self._hashed_string(password)

    def is_user(self):
        return True

    def is_admin(self):
        return self.role == 1

    def save(self):
        db.session.add(self)
        db.session.commit()

    def valid(self):
        valid_username = User.query.filter_by(username=self.username).first() == None
        valid_username_len = len(self.username) >= 3
        valid_password_len = len(self.password_hash) >= 3
        msgs = []
        if not valid_username:
            message = '用户名已经存在'
            msgs.append(message)
        elif not valid_username_len:
            message = '用户名长度必须大于等于 6'
            msgs.append(message)
        elif not valid_password_len:
            message = '密码长度必须大于等于 6'
            msgs.append(message)
        status = valid_username and valid_username_len and valid_password_len
        return status, msgs

    def validate_auth(self, form):
        username = form.get('username', '')
        password = form.get('password', '')
        username_equals = self.username == username
        password_equals = self.password_hash == self._hashed_string(password)
        return username_equals and password_equals

    def dict(self):
        d = {
            'username': self.username,
            'timestamp': self.timestamp,

        }
        return d

    #判断是否关注了uer_id
    def is_following(self, user_id):
        f = Follow.query.filter_by(
            follower_id=self.id, followed_id=user_id).first()
        return f is not None

    #判断是否被user_id关注
    def is_followed(self, user_id):
        f= Follow.query.filter_by(
            follower_id=user_id, followed_id=self.id).first()
        return f is not None

    def follow(self, user_id):
        if not self.is_following(user_id):
            f = Follow(follower_id=self.id, followed_id=user_id)
            f.save()

    def unfollow(self, user_id):
        f = Follow.query.filter_by(
            follower_id=self.id, followed_id=user_id).first()
        if f is not None:
            f.delete()

    def followed_posts(self):
        posts = Post.query.join(
            Follow, Post.user_id==Follow.followed_id
        ).filter(
            Follow.follower_id == self.id
        ).order_by(
            Post.timestamp.desc()
        ).all()
        return posts


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True),
                          default=sql.func.now())
    is_delete = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    ats = db.relationship('At', backref='post', lazy='dynamic')

    def __init__(self, form):
        self.content = form.get('post', None)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def dict(self):
        d = {
            'content': self.content,
            'timestamp': self.timestamp,
            'is_delete': self.is_delete,
            'comments': [comment.dict() for comment in self.comments],
        }
        return d


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True),
                          default=sql.func.now())
    is_delete = db.Column(db.Boolean, default=False)
    previous_comment_id =  db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    ats = db.relationship('At', backref='comment', lazy='dynamic')

    def __init__(self, form):
        self.content = form.get('comment', None)


    def save(self):
        db.session.add(self)
        db.session.commit()


    def previous_comment(self):
        reply = Comment.query.filter_by(id=self.previous_comment_id).first()
        log('debug reply user: ', reply.user)
        return reply


    def dict(self):
        d = {
            'content': self.content,
            'timestamp': self.timestamp,
            'is_delete': self.is_delete,
        }
        return d

class At(db.Model):
    __tablename__ = 'ats'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True),
                          default=sql.func.now())
    is_readed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return u'<At {}>'.format(self.id)


class ResponseData(object):
    def __init__(self, msgs=None, data=''):
        self.message = msgs
        self.data = data


    def success(self, next_url=''):
        self.success = True
        self.next = next_url
        return self.__dict__


    def error(self):
        self.success = False
        return self.__dict__




class AnonymousUser(object):
    def is_admin(self):
        return False

    def is_user(self):
        return False

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    print('数据库创建成功！')


