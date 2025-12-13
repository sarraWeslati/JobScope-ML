from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    cv_uploads = db.relationship('CVUpload', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat()
        }

class CVUpload(db.Model):
    __tablename__ = 'cv_uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    extracted_text = db.Column(db.Text)
    skills = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    matches = db.relationship('JobMatch', backref='cv_upload', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'skills': self.skills,
            'uploaded_at': self.uploaded_at.isoformat()
        }

class JobMatch(db.Model):
    __tablename__ = 'job_matches'
    
    id = db.Column(db.Integer, primary_key=True)
    cv_upload_id = db.Column(db.Integer, db.ForeignKey('cv_uploads.id'), nullable=False)
    job_title = db.Column(db.String(200))
    company = db.Column(db.String(200))
    location = db.Column(db.String(200))
    salary = db.Column(db.Float)
    required_skills = db.Column(db.Text)
    similarity_score = db.Column(db.Float)
    rank = db.Column(db.Integer)
    matched_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_title': self.job_title,
            'company': self.company,
            'location': self.location,
            'salary': self.salary,
            'required_skills': self.required_skills,
            'similarity_score': round(self.similarity_score, 4),
            'rank': self.rank
        }
