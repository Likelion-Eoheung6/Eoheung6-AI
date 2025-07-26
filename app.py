from flask import Flask
from service.config.qdrant_config import init_qdrant_collection
from service.config.qdrant_singleton import client


def create_app():
    app = Flask(__name__)

    # Qdrant ddl-auto = create로 설정
    init_qdrant_collection(client)

    # 컨트롤러 1
    @app.route('/ai', methods=['POST'])
    def callAi():
        # DB primary key
        user_id = request.json["user_id"]
        return 0

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5050)