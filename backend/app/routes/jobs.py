from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services.matching_service import get_matching_service

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/search', methods=['GET'])
@jwt_required()
def search_jobs():
    """Search jobs (optional endpoint for browsing)"""
    try:
        matching_service = get_matching_service()
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get jobs from dataset
        jobs_df = matching_service.jobs_df
        total = len(jobs_df)
        
        start = (page - 1) * per_page
        end = start + per_page
        
        jobs_page = jobs_df.iloc[start:end]
        
        jobs_list = []
        for _, job in jobs_page.iterrows():
            jobs_list.append({
                'job_title': job.get('job_title', 'N/A'),
                'company': job.get('company_name', job.get('company_location', 'N/A')),
                'location': job.get('company_location', 'N/A'),
                'salary': float(job.get('salary_usd', 0)),
                'required_skills': job.get('required_skills', 'N/A')
            })
        
        return jsonify({
            'jobs': jobs_list,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_job_stats():
    """Get job statistics"""
    try:
        matching_service = get_matching_service()
        jobs_df = matching_service.jobs_df
        
        stats = {
            'total_jobs': len(jobs_df),
            'avg_salary': float(jobs_df['salary_usd'].mean()) if 'salary_usd' in jobs_df.columns else 0,
            'top_locations': jobs_df['company_location'].value_counts().head(5).to_dict() if 'company_location' in jobs_df.columns else {},
            'top_titles': jobs_df['job_title'].value_counts().head(5).to_dict() if 'job_title' in jobs_df.columns else {}
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
