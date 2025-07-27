from flask import Blueprint, request, jsonify
from service.rag import vector_embed

rcmd_bp = Blueprint("rcmd", __name__, url_prefix="/ai")

@rcmd_bp.route("/", methods=["POST"])
def getRcmd():

    user_id = request.json.get("user_id")
    text = vector_embed(user_id)

    print(text)

    return jsonify({"message": f"{user_id}님을 위한 추천입니다."})