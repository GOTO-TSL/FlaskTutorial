import os

from flask import Flask

# Flaskインスタンスをグローバルに作成するために，関数の内側で作成し，appを返している
def create_app(test_config=None):
    # appの作成と設定
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # データを安全に保つためのFlaskの拡張機能
        SECRET_KEY="dev",
        # データベースを保存するパスの設定
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # インスタンスフォルダにconfig.pyがあれば標準設定を上書きする
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        # DBファイルを作成するためにインスタンスフォルダが作成されている必要がある
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 簡単なルーティングを行って確認
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from . import db
    db.init_app(app)

    return app