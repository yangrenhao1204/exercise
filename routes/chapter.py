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
from models.chapter import Chapter

main = Blueprint('chapter', __name__)


@main.route("/")
def index():
    chapter_list = Chapter.all()
    return render_template("chapter/chapter.html", chapters=chapter_list)


@main.route("/new")
def new():
    from models.subject import Subject
    subject_list = Subject.all()
    cookie = token_cookie()
    template = render_template(
        "chapter/edit_chapter.html",
        chapter=None,
        subjects=subject_list,
        token=cookie['token'],
    )
    r = make_response(template)
    r.set_cookie(cookie['token'], cookie['id'], max_age=300)
    return r


@main.route("/<int:chapter_id>")
def edit_chapter(chapter_id):
    c = Chapter.find(chapter_id)
    cookie = token_cookie()
    template = render_template(
        "chapter/edit_chapter.html",
        chapter=c,
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
        update_form = {
            'subject_id': int(form.get('subject_id', -1)),
            'name': form.get('name', ''),
            'article_id': int(form.get('article_id')) if form.get('article_id') != '' else -1,
        }
        Chapter.upsert(query_form, update_form)
        return redirect(url_for('.index'))
    else:
        abort(403)
