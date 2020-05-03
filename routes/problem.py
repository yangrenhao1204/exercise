from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    make_response,
    Response,
    abort,
)
from routes import *
from models.xls import XLS
from models.problem import Problem
import json


main = Blueprint('problem', __name__)


@main.route("/")
def index():
    problem_list = Problem.all()
    cookie = token_cookie()
    template = render_template(
        "problem/problem.html",
        problems=problem_list,
        token=cookie['token'],
    )
    # 如果要写入 cookie, 必须使用 make_response 函数
    # 然后再用 set_cookie 来设置 cookie
    r = make_response(template)
    r.set_cookie(cookie['token'], cookie['id'], max_age=300)
    return r


@main.route("/new")
def new():
    from models.subject import Subject
    from models.problem import Problem
    subject_list = Subject.all()
    problem_type = Problem.get_problem_type_list()
    cookie = token_cookie()
    template = render_template(
        "problem/new_problem.html",
        subjects=subject_list,
        types=problem_type,
        token=cookie['token'],
    )
    r = make_response(template)
    r.set_cookie(cookie['token'], cookie['id'], max_age=300)
    return r


@main.route("/<string:type>/<int:problem_id>")
def edit_problem(type, problem_id):
    p = Problem.find(type, problem_id)
    subject_name = Problem.get_subject_name(p.subject_id)
    chapter_name = Problem.get_chapter_name(p.chapter_id)
    cookie = token_cookie()
    template = render_template(
        "problem/edit_problem.html",
        problem=p,
        subject_name=subject_name,
        chapter_name=chapter_name,
        token=cookie['token'],
    )
    r = make_response(template)
    r.set_cookie(cookie['token'], cookie['id'], max_age=300)
    return r


@main.route("/delete")
def delete_problem():
    problem_id = int(request.args.get("problem_id"))
    type = request.args.get("type")
    if validate_legitimacy(request.args, request.cookies):
        Problem.delete(type, problem_id)
        return redirect(url_for('.index'))
    else:
        abort(403)


@main.route("/add", methods=['POST'])
def add():
    form = request.form
    if validate_legitimacy(form, request.cookies):
        Problem.upsert(form)
        return redirect(url_for('.index'))
    else:
        abort(403)


@main.route("/get_chapter_list")
def get_chapter_list():
    args = request.args
    chapter_list = []
    from models.chapter import Chapter
    chapters = Chapter.find_all(subject_id=int(args['subject_id']))
    for c in chapters:
        chapter_list.append(c.json())
    return Response(json.dumps(chapter_list),content_type='application/json')


@main.route("/upload_file", methods=['POST'])
def read_file():
    form = request.form
    if validate_legitimacy(form, request.cookies):
        problem_list = XLS.add_record(request.files['file'])
        Problem.add_problem_from_xls(problem_list)
        return redirect(url_for('.index'))
    else:
        abort(403)
