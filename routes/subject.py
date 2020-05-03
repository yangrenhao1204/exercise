from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
)
from routes import *
from models.subject import Subject

main = Blueprint('subject', __name__)


@main.route("/")
def index():
    subject_list = Subject.all()
    return render_template("subject/subject.html", subjects=subject_list)


@main.route("/new")
def new():
    cookie = token_cookie()
    template = render_template(
        "subject/edit_subject.html",
        subject=None,
        token=cookie['token'],
    )
    r = make_response(template)
    r.set_cookie(cookie['token'], cookie['id'], max_age=300)
    return r


@main.route("/<int:subject_id>")
def edit_subject(subject_id):
    cookie = token_cookie()
    s = Subject.find(subject_id)
    template = render_template(
        "subject/edit_subject.html",
        subject=s,
        token=cookie['token'],
    )
    r = make_response(template)
    r.set_cookie(cookie['token'], cookie['id'], max_age=300)
    return r


@main.route("/add", methods=['POST'])
def add():
    form = request.form
    if validate_legitimacy(form, request.cookies):
        query_form = {
            'id': int(form.get('id'))
        }
        update_form = {}
        for k, v in form.items():
            if k != 'id':
                update_form[k] = v
        Subject.upsert(query_form, update_form)
        return redirect(url_for('.index'))
    else:
        abort(403)


# @main.route("/delete")
# def delete_subject_by_id(subject_id):
#     subject_id = int(request.args.get("subject_id"))
#     Subject.delete_by_id(subject_id)
#     return redirect(url_for('.index'))
