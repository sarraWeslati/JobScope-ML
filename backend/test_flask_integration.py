"""
Quick API integration test to verify LDA model works with the Flask app
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Set up Flask app context
from app import create_app

app = create_app()

with app.app_context():
    print("=" * 80)
    print("TESTING LDA MODEL IN FLASK CONTEXT")
    print("=" * 80)
    
    from app.services.cv_matching_service import get_cv_matching_service
    
    print("\n[1/2] Loading service in Flask context...")
    service = get_cv_matching_service()
    print("✅ Service loaded successfully in Flask app")
    
    print("\n[2/2] Testing CV matching...")
    test_cv = """
    Senior Data Scientist with 8 years of experience in machine learning, 
    deep learning, and artificial intelligence. Expert in Python, TensorFlow, 
    PyTorch, and scikit-learn. Strong background in NLP, computer vision, 
    and statistical modeling. Proficient in cloud platforms (AWS, GCP) and 
    big data technologies (Spark, Hadoop).
    """
    
    result = service.match_cv(test_cv, top_n=3)
    
    if result['success']:
        print("✅ Matching successful!")
        print(f"   Model: {result.get('model_type', 'N/A')}")
        print(f"   Topics: {result.get('n_topics', 'N/A')}")
        print(f"\n   Top 3 matches:")
        for match in result['matches']:
            print(f"   {match['rank']}. {match['job_title']} at {match['company']} - {match['similarity_score']*100:.2f}%")
    else:
        print(f"❌ Matching failed: {result.get('error', 'Unknown')}")
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print("✅ FLASK INTEGRATION TEST PASSED!")
    print("=" * 80)
    print("\n🎉 The API is ready to serve requests with the LDA model!")
