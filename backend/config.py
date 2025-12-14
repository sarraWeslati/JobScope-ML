import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Database Configuration
    # Set DATABASE_URL for external MySQL (PlanetScale, Railway, etc.)
    # Or use MYSQL_* vars for local MySQL
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        SQLALCHEMY_DATABASE_URI = database_url
    elif os.environ.get('MYSQL_USER') or os.environ.get('MYSQL_PASSWORD'):
        # Local MySQL via individual vars
        SQLALCHEMY_DATABASE_URI = \
            f"mysql+pymysql://{os.environ.get('MYSQL_USER', 'root')}:" \
            f"{os.environ.get('MYSQL_PASSWORD', '')}@" \
            f"{os.environ.get('MYSQL_HOST', 'localhost')}:" \
            f"{os.environ.get('MYSQL_PORT', '3306')}/" \
            f"{os.environ.get('MYSQL_DATABASE', 'job_matching')}"
    else:
        raise ValueError("No database configured. Set DATABASE_URL or MYSQL_* environment variables.")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
    
    JOBS_DATASET_PATH = os.path.join(os.path.dirname(__file__), 'data', 'ai_job_dataset.csv')
    CV_DATASET_PATH = os.path.join(os.path.dirname(__file__), 'data', 'dataset_cvs_cleaned.csv')
    
    CORS_HEADERS = 'Content-Type'
    # Comma-separated list of allowed origins, e.g.
    # "http://localhost:3000,http://localhost:3001,https://jobscopeml.vercel.app"
    ALLOWED_ORIGINS = [origin.strip() for origin in (
        os.environ.get('ALLOWED_ORIGINS') or 
        'http://localhost:3000,http://localhost:3001,https://jobscopeml.vercel.app'
    ).split(',') if origin.strip()]
