from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
# blog のBlueprintを作成 blogはこのアプリの主機能なのでurl_prefixを持たない
bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    post = db.execute(
        'SELECT p.id, title, body, created, auther_id, username'
        ' FROM post p JOIN user u ON p.auther_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)