from flask import (
    request,
    Blueprint,
    Response,
    jsonify,
)
import requests, json
from bson import json_util
import config.miniprogram_config as config

from models.user import User
from models.subject import Subject
from models.chapter import Chapter
from models.article import Article
from models.problem import Problem
from models.error_set import ErrorSet

main = Blueprint('miniprogram', __name__)


@main.route('/login', methods=["GET", "POST"])
def login():
    data = request.values
    code = data['code']  # 前端POST过来的微信临时登录凭证code
    req_params = {
        'appid': config.AppID,
        'secret': config.AppSecret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    wx_login_api = 'https://api.weixin.qq.com/sns/jscode2session'
    response_data = requests.get(wx_login_api, params=req_params)  # 向API发起GET请求
    data = response_data.json()
    openid = data['openid']  # 得到用户关于当前小程序的OpenID
    # session_key = data['session_key'] #得到用户关于当前小程序的会话密钥session_key
    # 保存用户信息
    return json.dumps({'openid': openid}, ensure_ascii=False)


@main.route('/saveUserInfo', methods=["POST"])
def saveUserInfo():
    form = json.loads(request.get_data(as_text=True))
    if (form["openid"] != ""):
        query_form = {
            'openid': form["openid"],
        }
        u = User.upsert(query_form, form)
        return "ok"


@main.route('/getSubjectList')
def get_subject_list():
    all_subject = Subject.all()
    subject_list = [s.__dict__ for s in all_subject]
    return Response(json_util.dumps(subject_list, ensure_ascii=False), content_type='application/json')


@main.route('/getChapterList', methods=["POST"])
def get_chapter_list():
    form = json.loads(request.get_data(as_text=True))
    all_chapter = Chapter.find_all(subject_id=form["subject_id"])
    chapter_list = [c.__dict__ for c in all_chapter]
    return Response(json_util.dumps(chapter_list, ensure_ascii=False), content_type='application/json')


@main.route('/getProblemList', methods=["POST"])
def get_problem_list():
    form = json.loads(request.get_data(as_text=True))
    all_problem = Problem.find_all(subject_id=form["subject_id"])
    return Response(json_util.dumps(all_problem, ensure_ascii=False), content_type='application/json')


@main.route('/getErrorProblemIdSet', methods=["POST"])
def get_error_set():
    form = json.loads(request.get_data(as_text=True))
    error_set = ErrorSet.get_error_set(form)
    return Response(json_util.dumps(error_set, ensure_ascii=False), content_type='application/json')


@main.route('/saveErrorProblemIdSet', methods=["POST"])
def save_error_set():
    form = json.loads(request.get_data(as_text=True))
    ErrorSet.save_error_set(form)
    return 'ok'


@main.route('/getArticle', methods=["POST"])
def get_article():
    form = json.loads(request.get_data(as_text=True))
    article = Article.find_by(chapter_id=form["chapter_id"])
    if article == None:
        article = Article()
        article.title = "空"
        article.content = "当前章节没有文章,请直接刷题"
        return Response(json.dumps(article.__dict__, ensure_ascii=False), content_type='application/json')
    else:
        return Response(json_util.dumps(article.__dict__, ensure_ascii=False), content_type='application/json')