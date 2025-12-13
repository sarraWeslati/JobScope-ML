"""
Enhanced production server with better logging and CORS
"""

import os
import sys
import logging
try:
    from waitress import serve
    _USE_WAITRESS = True
except ModuleNotFoundError:
    serve = None
    _USE_WAITRESS = False
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the Flask app
logger.info("Creating Flask app...")
app = create_app()
logger.info("Flask app created successfully!")

# Log CORS configuration
logger.info("CORS Configuration:")
logger.info(f"  - Origins: http://localhost:3000, http://localhost:3001, https://jobscopeml.vercel.app")
logger.info(f"  - Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH")
logger.info(f"  - Headers: Content-Type, Authorization, X-Requested-With")

# Test route
@app.route("/", methods=["GET"])
def home():
    logger.info("Health check requested")
    return {
        "status": "API is running",
        "service": "JobScope-ML",
        "environment": os.environ.get('FLASK_ENV', 'development')
    }, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    
    logger.info("=" * 70)
    logger.info("Starting JobScope-ML API")
    logger.info(f"Port: {port}")
    logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    logger.info("=" * 70)
    
    if _USE_WAITRESS:
        logger.info("Using Waitress WSGI server")
        try:
            serve(
                app,
                host="0.0.0.0",
                port=port,
                threads=4,
                _quiet=False
            )
        except Exception as e:
            logger.error(f"Failed to start Waitress: {e}")
            sys.exit(1)
    else:
        logger.warning("Waitress not installed; falling back to Flask's built-in server")
        try:
            app.run(host="0.0.0.0", port=port)
        except Exception as e:
            logger.error(f"Failed to start Flask dev server: {e}")
            sys.exit(1)
