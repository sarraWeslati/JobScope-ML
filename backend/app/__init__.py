from flask import Flask, after_this_request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config
import os
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def add_cors_headers(response):
    """Deprecated: CORS handled by Flask-CORS. Keep for backward-compat."""
    return response

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    # Enable CORS for API routes
    CORS(
        app,
        resources={r"/api/*": {"origins": Config.ALLOWED_ORIGINS}},
        supports_credentials=True,
        expose_headers=["Content-Type", "Authorization"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        max_age=3600
    )
    
    # Let Flask-CORS manage response headers; avoid overriding allowed origins
    @app.after_request
    def after_request(response):
        return response
    
    # Handle OPTIONS requests explicitly
    @app.before_request
    def handle_preflight():
        from flask import request
        if request.method == 'OPTIONS':
            # Rely on Flask-CORS to generate proper preflight response
            return app.make_default_options_response(), 200
    
    # Register JWT error handlers
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'error': 'Invalid token', 'message': str(error)}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'error': 'Missing authorization token'}, 401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token has expired'}, 401
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.jobs import jobs_bp
    from app.routes.cv import cv_bp
    from app.routes.health import health_bp
    
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(jobs_bp, url_prefix='/api/jobs')
    app.register_blueprint(cv_bp, url_prefix='/api/cv')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
