from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    make_response,
    abort,
)
import json
from bson import json_util
from routes import *
from models.article import Article

main = Blueprint('article', __name__)


@main.route("/")
def index():
    article_list = Article.all()
    return render_template("article/article.html", articles=article_list)


@main.route("/new")
def new():
    from models.subject import Subject
    subject_list = Subject.all()
    obj = Article.get_subject_and_chapter_name()
    cookie = token_cookie()
    template = render_template(
        "article/edit_article.html",
        article=None,
        subjects=subject_list,
        obj=json_util.dumps(obj),
        token=cookie['token'],
    )
    r = make_response(template)
    r.set_cookie(cookie['token'], cookie['id'], max_age=300)
    return r


@main.route("/<int:article_id>")
def edit_article(article_id):
    a = Article.find(article_id)
    cookie = token_cookie()
    template = render_template(
        "article/edit_article.html",
        article=a,
        token=cookie['token'],
    )
    r = make_response(template)
    r.set_cookie(cookie['token'], cookie['id'], max_age=1200)
    return r


@main.route("/add", methods=['POST'])
def add():
    form = request.form
    if validate_legitimacy(form, request.cookies):
        Article.save_article(form)
        return redirect(url_for('.index'))
    else:
        abort(403)
