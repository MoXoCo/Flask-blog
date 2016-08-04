from .. import db

import time


class ReprMixin(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)

def created_time():
    t = time.time()
    localtime = time.localtime(t)
    patten = '%Y-%m-%d %H:%M:%S'
    tt = time.strftime(patten,localtime)
    return tt

from .follow import Follow
from .post import Post
from .user import User
from .comment import Comment
from .at import At