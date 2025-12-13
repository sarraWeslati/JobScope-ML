"""
Production-ready server using Waitress
"""

import os
from waitress import serve
from flask_cors import CORS
from app import create_app   # your app factory

# Create the Flask app
app = create_app()

# Configure CORS for production
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",  # Local development
            "http://localhost:3001",  # Local development alternative
            "https://jobscopeml.vercel.app",  # Production frontend
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Optional health check
@app.route("/")
def home():
    return {
        "status": "API is running",
        "service": "JobScope-ML"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    print("=" * 60)
    print("Starting JobScope-ML API with Waitress")
    print(f"Running on port {port}")
    print("=" * 60)

    serve(
        app,
        host="0.0.0.0",
        port=port,
        threads=4
    )
