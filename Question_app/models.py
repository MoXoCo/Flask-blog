from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from One_Index import One_Index_Spider
from mylog import log


from datetime import datetime

db_path = 'db.sqlite'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///{}'.format(db_path)
app.secret_key = 'a random string'

db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    url_num = db.Column(db.Integer)
    title = db.Column(db.String(10))
    img = db.Column(db.String(64))
    content = db.Column(db.String())
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), default='游客')
    img = db.Column(db.String(64), default='http://placekitten.com/80/80')
    content = db.Column(db.String())
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))


    def __init__(self, content):
        self.content = content


    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        extra = dict(
            post_id = self.post_id,
        )
        d = {k: v for k, v in self.__dict__.items() if k not in self.blacklist()}
        d.update(extra)
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
        ]
        return b



def update():
    one_index = One_Index_Spider()
    # one的格式是 { url_num: [title, content, img]}
    one = one_index.run
    for key, value in one.items():
        if not Post.query.filter_by(url_num=int(key)).first():
            post = Post()
            post.url_num = key
            post.title, post.content, post.img = value
            post.save()
        else:
            log('{} 已在数据库中'.format(key))

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    update()
    log('数据库创建成功！')

