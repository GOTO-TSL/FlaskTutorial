import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# authという名前のBlueprintを作成する
# appと同様にどこに定義されているか知る必要があるため第2引数に__name__がある
# url_prefixはblueprintと関連付けられるすべてのパスの先頭に/authがつけられるということ

bp = Blueprint("auth", __name__, url_prefix="/auth")

### View関数の前に実行する関数を登録 ###
@bp.before_app_request
def load_logged_in_user():
    # sessionにuser_idが格納されているかをチェックし，あればg.userにそのユーザーidのユーザーを格納
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()

### 登録のView ###
@bp.route("/register", methods=("GET", "POST"))
def register():
    # ユーザーがフォームを送信した場合request.methodはPOSTになり，入力データの検証を行う
    if request.method == "POST":
        # request.formは提出されたformのキーと値を対応付ける特別なdictオブジェクト
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        # 空かどうかを検証
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        # 登録済みでないかを検証
        # db.executeはSQLクエリとtupleが引数にあり，?にtupleの中身が入ったクエリになる
        elif db.execute(
            "SELECT id FROM user WHERE username = ?", (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."
        
        if error is None:
            # 検証が正常に終了した場合．DBに保存する
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            # DBに変更を加えた後は必ずdb.commit()
            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")

### ログインのView ###
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # ユーザーの情報は後ほど使用するために変数に格納しておく
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # パスワードの検証
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        # sessionはリクエストを跨いで格納されるデータのdict
        # ユーザーのidはsessionに格納されてこれ以降のリクエストで利用可能になる
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

### ログアウト ###
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

### デコレーター ###
# 各Viewでログインされているかどうかチェックできるようにする
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        
        return view(**kwargs)
    return wrapped_view