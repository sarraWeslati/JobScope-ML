"""
Production-ready server using Waitress
"""
from waitress import serve
from app import create_app

if __name__ == '__main__':
    print("="*60)
    print("Starting Job Matching API with Waitress")
    print("="*60)
    
    app = create_app()
    
    print("App created successfully")
    print("Server starting on http://localhost:5000")
    print("="*60)
    print("Press Ctrl+C to stop")
    print()
    
    serve(app, host='0.0.0.0', port=5000, threads=4)
