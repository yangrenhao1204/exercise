from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    make_response,
)
from routes import *

main = Blueprint('admin', __name__)


@main.route('/')
@main.route('/profile')
def profile():
    a = current_admin()
    if a is None:
        return redirect(url_for('.request_login'))
    else:
        return render_template('admin/profile.html', admin=a)


@main.route('/request_register')
def request_register():
    return render_template('admin/register.html')


@main.route('/request_login')
def request_login():
    return render_template('admin/login.html')


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    a = Admin.register(form)
    if a is None:
        return redirect(url_for('.request_register'))
    else:
        session['admin_id'] = a.id
        return redirect(url_for('index.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    a = Admin.validate_login(form)
    if a is None:
        return redirect(url_for('.request_login'))
    else:
        # session 中写入 id
        session['admin_id'] = a.id
        return redirect(url_for('index.index'))
