from flask import Blueprint, request, jsonify
from app.services.matching_service import get_matching_service

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Backend is running',
        'api_version': '1.0.0'
    }), 200

@health_bp.route('/test-match', methods=['POST'])
def test_match():
    """Test matching without authentication"""
    try:
        data = request.get_json()
        if not data or 'cv_text' not in data:
            return jsonify({'error': 'cv_text required in body'}), 400
        
        matching_service = get_matching_service()
        result = matching_service.find_top_matches(data['cv_text'], top_n=5)
        
        return jsonify(result), 200 if result['success'] else 500
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500
