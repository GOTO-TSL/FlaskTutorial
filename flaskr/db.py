# SQLite3を使用，別でサーバーを用意することなく簡単に使える
# 並列なデータを同時に書き込もうとする場合，それらが直列に処理されるために遅くなってしまうので
# そのような場合には別のデータベースを選択する必要がある
import sqlite3

import click
from flask import current_app, g
from flask import cli
from flask.cli import with_appcontext

def init_app(app):
    # レスポンスを返した後，クリーンアップを行っているときにclose_dbを呼び出す
    app.teardown_appcontext(close_db)
    # flaskコマンドで呼び出せるコマンドを追加
    app.cli.add_command(init_db_command)

# DBの作成
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode("utf-8"))

# init-dbと呼ばれるコマンドを作成する．内容は以下の関数内
@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database")    

# DBの接続を行う．操作する際にまずはconnection
def get_db():
    # 'g'は特別なオブジェクトでリクエストごとに個別のものになる
    if "db" not in g:
        g.db = sqlite3.connect(
            # current_appはinit.pyで作成しているappインスタンスを指すことになる
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db
# g.dbが設定されているかどうかしらべることでconnection作成済みかどうかを調べる
# connectionがあれば閉じる．
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()