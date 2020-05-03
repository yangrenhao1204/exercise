from flask import (
    Flask,
)
from routes.admin import main as admin_routes
from routes.miniprogram import main as miniprogram_routes
from routes.subject import main as subject_routes
from routes.chapter import main as chapter_routes
from routes.article import main as article_routes
from routes.problem import main as problem_routes
from routes.index import main as index_routes

app = Flask(__name__)
app.secret_key = 'exercise'

app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(miniprogram_routes, url_prefix='/miniprogram')
app.register_blueprint(subject_routes, url_prefix='/subject')
app.register_blueprint(chapter_routes, url_prefix='/chapter')
app.register_blueprint(article_routes, url_prefix='/article')
app.register_blueprint(problem_routes, url_prefix='/problem')
app.register_blueprint(index_routes)


@app.errorhandler(404)
def page_not_found(error):
    return error


# 运行代码
if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2100,
    )
    app.run(**config)
