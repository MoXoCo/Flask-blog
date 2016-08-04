from . import db
from . import ReprMixin
from . import created_time

class Follow(db.Model, ReprMixin):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.String(), default=created_time)

    def __repr__(self):
        return u'<User({}) follow User({})>'.format(
            self.follow_id, self.followed_id
        )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()