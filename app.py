import os
from dotenv import load_dotenv
from flask import Flask
from service.config.qdrant_config import init_qdrant_collection
from service.config.qdrant_singleton import client
from service.config.sql_alchemy import db


def create_app():
    load_dotenv()

    app = Flask(__name__)

    MYSQL_URL = os.environ.get("DATABASE_URL")

    app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    # Qdrant ddl-auto = create로 설정
    init_qdrant_collection(client)

    # 컨트롤러 등록

    print("컨트롤러 진입")

    from controller.getRcmd import rcmd_bp
    app.register_blueprint(rcmd_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.run(host="0.0.0.0", port=5050)