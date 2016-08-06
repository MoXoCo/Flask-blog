from . import db
from . import ReprMixin
from . import created_time
from . import Follow
from . import Post



class User(db.Model, ReprMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String(), unique=True)
    timestamp = db.Column(db.String(), default=created_time)
    role = db.Column(db.Integer, default=2)
    img = db.Column(db.String(), default='/static/img/1.jpg')
    address = db.Column(db.String())
    profession = db.Column(db.String())
    company = db.Column(db.String())
    position = db.Column(db.String())
    education = db.Column(db.String())
    signature = db.Column(db.String())
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

    @staticmethod
    def user_by_name(username):
        return User.query.filter_by(username=username).first()


    def __init__(self, form):
        self.username = form.get('username', None)
        self.password = form.get('password', None)
        self.followed.append(Follow(followed=self, follower=self))
        if self.username == 'admin':
            self.role = 1


    def save_personal_msg(self, form):
        self.address = form.get('address', '')
        self.profession = form.get('profession', '')
        self.company = form.get('company', '')
        self.position = form.get('position', '')
        self.education = form.get('education', '')
        self.signature = form.get('signature', '')
        self.save()

    def personal_msg(self):
        form = dict(
            username=self.username,
            address=self.address,
            profession=self.profession,
            company=self.company,
            position=self.position,
            education=self.education,
            signature=self.signature,
        )
        return form


    def json(self):
        self.id
        d = {k: v for k, v in self.__dict__.items() if k not in self.blacklist()}
        return d


    def blacklist(self):
        b = [
            '_sa_instance_state',
            'password',
        ]
        return b


    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def is_admin(self):
        return self.role == 1


    def validate_auth(self, form):
        username = form.get('username', '')
        password = form.get('password', '')
        username_equals = self.username == username
        password_equals = self.password == password
        print('validate auth', username, password, username_equals, password_equals)
        return username_equals and password_equals


    def register_validate(self):
        min_len = 3
        valid_username = User.query.filter_by(username=self.username).first() == None
        valid_username_len = len(self.username) >= min_len
        valid_password_len = len(self.password) >= min_len
        msgs = []
        if not valid_username:
            message = '用户名已经存在'
            msgs.append(message)
        elif not valid_username_len:
            message = '用户名长度必须大于等于 3'
            msgs.append(message)
        elif not valid_password_len:
            message = '密码长度必须大于等于 3'
            msgs.append(message)
        status = valid_username and valid_username_len and valid_password_len
        return status, msgs

    # 判断是否关注了uer_id
    def is_following(self, user_id):
        f = Follow.query.filter_by(
            follower_id=self.id, followed_id=user_id).first()
        return f is not None

    # 判断是否被user_id关注
    def is_followed(self, user_id):
        f = Follow.query.filter_by(
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
            Follow, Post.user_id == Follow.followed_id
        ).filter(
            Follow.follower_id == self.id
        ).filter(
            Post.is_delete == False
        ).order_by(
            Post.timestamp.desc()
        ).all()
        return posts

    def user_ated_num(self):
        ated_num = self.ats.filter_by(is_readed=False).count()
        return ated_num


