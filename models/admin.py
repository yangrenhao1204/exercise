from models.mongo import Mongo
from models import Model


# class Admin(Model):
#     def __init__(self, form):
#         self.id = int(form.get('id', -1))
#         self.name = form.get('name', '')
#         self.password = form.get('password', '')
#         self.avatar_url = form.get('avatar_url', '')

class Admin(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('name', str, ''),
        ('password', str, ''),
        ('avatar_url', str, ''),
    ]

    def __init__(self):
        self.avatarUrl = 'default.png'

    @staticmethod
    def salted_password(password, salt='$![]y%Y&L@r*X#F%h()'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    @classmethod
    def register(cls, form):
        name = form.get('name', '')
        pwd = form.get('password', '')
        if len(name) > 2 and Admin.find_by(name=name) is None:
            a = Admin.new(form)
            a.password = a.salted_password(pwd)
            a.save()
            return a
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        a = cls()
        for k, v in form.items():
            setattr(a, k, v)
        admin = Admin.find_by(name=a.name)
        if admin is not None and admin.password == a.salted_password(a.password):
            return admin
        else:
            return None
