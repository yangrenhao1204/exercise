from flask import session
import uuid
from models.admin import Admin


def current_admin():
    aid = session.get('admin_id', -1)
    a = Admin.find_by(id=aid)
    return a


def token_cookie():
    token = str(uuid.uuid4())
    a = current_admin()
    token_cookie = dict(
        token=token,
        id=str(a.id if a is not None else -1),
    )
    return token_cookie


def validate_legitimacy(args, cookies):
    token = args.get("token", default=None)
    cookie_admin_id = -1
    if cookies.get(token) != None:
        cookie_admin_id = int(cookies.get(token))
    a = current_admin()
    if a is not None and a.id == cookie_admin_id:
        return True
    else:
        return False
