from flask import Flask

app = Flask(__name__)

@app.route('/ai', methods=['POST'])
def callAi():
    # DB primary key
    user_id = request.json["user_id"]
    return 0

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)