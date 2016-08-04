from . import db
from . import ReprMixin
from . import created_time
import random

class Post(db.Model, ReprMixin):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.String(), default=created_time)
    is_delete = db.Column(db.Boolean, default=False)
    direction = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    ats = db.relationship('At', backref='post', lazy='dynamic')

    def __init__(self, form):
        self.content = form.get('post', None)
        self.direction = random.choice(['left', 'right'])


    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        extra_data = dict(
            img=self.user.img,
            username=self.user.username,
        )
        d = {k: v for k, v in self.__dict__.items() if k not in self.blacklist()}
        d.update(extra_data)
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
            'user',
        ]
        return b
