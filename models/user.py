from models.mongo import Mongo
from models import Model
from models.error_set import ErrorSet


# class User(Model):
#     def __init__(self, form):
#         self.id = int(form.get('id', -1))
#         self.openid = form.get('openid', '')
#         # self.session_key = form.get('session_key', '')
#         self.nickname = form.get('nickname', '')
#         self.avatar_url = form.get('avatar_url', 'user_default.png')

class User(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('openid', str, ''),
        # ('session_key', str, ''),
        ('nickname', str, ''),
        ('avatar_url', str, ''),
    ]

    def __init__(self):
        self.avatarUrl = 'user_default.png'
