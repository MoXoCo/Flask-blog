from . import db
from . import ReprMixin
from . import created_time


class At(db.Model, ReprMixin):
    __tablename__ = 'ats'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(), default=created_time)
    is_readed = db.Column(db.Boolean, default=False)
    is_delete = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))

    def __init__(self, u_id, p_id, c_id=None):
        self.user_id = u_id
        self.post_id = p_id
        self.comment_id = c_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        self.is_delete = True
        self.save()

    def json(self):
        extra_data = dict(
            username=self.user.username,
            post=self.post.content,
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