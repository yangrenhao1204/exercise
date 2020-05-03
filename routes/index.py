from flask import (
    render_template,
    Blueprint,
)


main = Blueprint('index', __name__)


@main.route("/")
def index():
    return render_template("index/index.html")
