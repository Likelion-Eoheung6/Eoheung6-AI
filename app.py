import os
from dotenv import load_dotenv
from flask import Flask
from service.config.qdrant_config import init_qdrant_collection
from service.config.sql_alchemy import db
from service.model.class_model import Class, ClassOpen


def create_app():
    load_dotenv()

    app = Flask(__name__)

    MYSQL_URL = os.environ.get("DATABASE_URL")

    app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    # 스키마 새로 선언 <- 추후 삭제해야 할 부분 FIXME
    with app.app_context():
        db.create_all()
    # Qdrant ddl-auto = create로 설정
    init_qdrant_collection()

    # 컨트롤러 등록

    print("컨트롤러 진입")

    from controller.save_data import save_bp
    from controller.get_answer import call_bp
    app.register_blueprint(save_bp)
    app.register_blueprint(call_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.run(host="0.0.0.0", port=5050)

    