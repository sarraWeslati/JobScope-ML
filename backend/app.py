from flask import Flask, request, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/auth/register", methods=["POST"])
    def register():
        data = request.json
        return jsonify({
            "message": "Register endpoint working",
            "data": data
        })

    return app
