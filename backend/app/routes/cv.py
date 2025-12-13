from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import CVUpload, JobMatch
from app.utils.file_handler import save_uploaded_file, extract_text_from_file
from app.services.cv_matching_service import get_cv_matching_service

cv_bp = Blueprint('cv', __name__)

@cv_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_cv():
    """Upload CV and find top 5 job matches using LDA"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file
        file_path, filename = save_uploaded_file(file, user_id)
        
        if not file_path:
            return jsonify({'error': 'Invalid file type. Allowed: PDF, DOCX, TXT'}), 400
        
        # Extract text from file
        extracted_text = extract_text_from_file(file_path)
        
        if not extracted_text or extracted_text.strip() == '':
            return jsonify({'error': 'Could not extract text from file or file is empty'}), 400
        
        # Get CV matching service (LDA based)
        cv_matching_service = get_cv_matching_service()
        
        # Find top 5 job matches
        result = cv_matching_service.match_cv(extracted_text, top_n=5)
        
        if not result['success']:
            return jsonify({'error': result.get('error', 'Matching failed')}), 500
        
        # Save CV upload to database
        cv_upload = CVUpload(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            extracted_text=extracted_text[:1000],  
            skills='TF-IDF Matched'  
        )
        db.session.add(cv_upload)
        db.session.flush()  # Get the cv_upload.id
        
        # Save job matches
        for match in result['matches']:
            job_match = JobMatch(
                cv_upload_id=cv_upload.id,
                job_title=match['job_title'],
                company=match['company'],
                location=match['location'],
                salary=match['salary'],
                required_skills=match['required_skills'],
                similarity_score=match['similarity_score'],
                rank=match['rank']
            )
            db.session.add(job_match)
        
        db.session.commit()
        
        return jsonify({
            'message': 'CV uploaded successfully',
            'cv_id': cv_upload.id,
            'top_5_matches': result['matches'],
            'total_jobs_searched': result['total_jobs_searched'],
            'cv_text_length': result['cv_length']
        }), 201
        
    except Exception as e:
        db.session.rollback()
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in CV upload: {error_details}")  # Log to console
        return jsonify({
            'error': 'Internal server error during CV upload',
            'details': str(e)
        }), 500

@cv_bp.route('/history', methods=['GET'])
@jwt_required()
def get_cv_history():
    """Get user's CV upload history"""
    try:
        user_id = int(get_jwt_identity()) 
        
        cv_uploads = CVUpload.query.filter_by(user_id=user_id)\
            .order_by(CVUpload.uploaded_at.desc())\
            .all()
        
        history = []
        for cv in cv_uploads:
            matches = [match.to_dict() for match in cv.matches]
            history.append({
                **cv.to_dict(),
                'matches': matches
            })
        
        return jsonify({'history': history}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cv_bp.route('/<int:cv_id>', methods=['GET'])
@jwt_required()
def get_cv_details(cv_id):
    """Get specific CV upload details with matches"""
    try:
        user_id = int(get_jwt_identity()) 
        
        cv_upload = CVUpload.query.filter_by(id=cv_id, user_id=user_id).first()
        
        if not cv_upload:
            return jsonify({'error': 'CV not found'}), 404
        
        matches = [match.to_dict() for match in cv_upload.matches]
        
        return jsonify({
            'cv': cv_upload.to_dict(),
            'matches': matches
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cv_bp.route('/<int:cv_id>', methods=['DELETE'])
@jwt_required()
def delete_cv(cv_id):
    """Delete a CV upload"""
    try:
        user_id = int(get_jwt_identity())  
        
        cv_upload = CVUpload.query.filter_by(id=cv_id, user_id=user_id).first()
        
        if not cv_upload:
            return jsonify({'error': 'CV not found'}), 404
        
        db.session.delete(cv_upload)
        db.session.commit()
        
        return jsonify({'message': 'CV deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cv_bp.route('/dataset/statistics', methods=['GET'])
def get_cv_dataset_statistics():
    """Get statistics from the CV dataset"""
    try:
        matching_service = get_matching_service()
        
        if matching_service.cvs_df.empty:
            return jsonify({
                'message': 'CV dataset not available',
                'stats': {}
            }), 200
        
        cvs_df = matching_service.cvs_df
        stats = {
            'total_cvs': len(cvs_df),
            'columns': list(cvs_df.columns),
            'sample_skills': cvs_df['skills'].unique()[:10].tolist() if 'skills' in cvs_df.columns else [],
            'data_quality': {
                'missing_values': cvs_df.isnull().sum().to_dict(),
                'duplicates': int(cvs_df.duplicated().sum())
            }
        }
        
        return jsonify({
            'message': 'CV dataset statistics retrieved',
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cv_bp.route('/dataset/sample', methods=['GET'])
def get_cv_dataset_sample():
    """Get sample CVs from the dataset"""
    try:
        matching_service = get_matching_service()
        
        if matching_service.cvs_df.empty:
            return jsonify({
                'message': 'CV dataset not available',
                'samples': []
            }), 200
        
        limit = request.args.get('limit', 5, type=int)
        samples = matching_service.cvs_df.head(limit).to_dict('records')
        
        return jsonify({
            'message': 'Sample CVs retrieved',
            'samples': samples,
            'total': len(matching_service.cvs_df)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cv_bp.route('/matching-stats', methods=['GET'])
def get_matching_stats():
    """Get statistics about the matching system"""
    try:
        cv_matching_service = get_cv_matching_service()
        stats = cv_matching_service.get_job_stats()
        
        return jsonify({
            'message': 'Matching system stats',
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

