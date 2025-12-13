#!/usr/bin/env python
"""
Test the LDA-based matching API without Flask running
This tests the services directly
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.cv_matching_service import CVMatchingService
from app.services.matching_service import JobMatchingService
import pandas as pd


def test_cv_matching_service():
    """Test CVMatchingService with LDA model"""
    print("\n" + "="*80)
    print("TESTING CV MATCHING SERVICE WITH LDA MODEL")
    print("="*80)
    
    try:
        service = CVMatchingService()
        print("✅ CVMatchingService initialized successfully")
        
        # Test with sample CV text
        sample_cv = """
        Python Developer with 5 years experience.
        Skills: Python, Django, REST APIs, PostgreSQL, Docker, Kubernetes
        Experience: Led development of microservices architecture
        Education: BS Computer Science
        """
        
        print("\n[Test 1] Matching sample CV text...")
        result = service.match_cv(sample_cv, top_n=5)
        
        if result and result.get('success'):
            match_list = result.get('matches', [])
            if match_list:
                print(f"✅ Got {len(match_list)} job matches:")
                for i, match in enumerate(match_list, 1):
                    score = match.get('similarity_score', 0) * 100
                    print(f"   {i}. {match.get('job_title')} - Score: {score:.2f}%")
            else:
                print("❌ No matches in result")
        else:
            error = result.get('error') if isinstance(result, dict) else str(result)
            print(f"❌ Error: {error}")
            
    except Exception as e:
        print(f"❌ Error in CVMatchingService: {str(e)}")
        import traceback
        traceback.print_exc()


def test_matching_service():
    """Test JobMatchingService with LDA model"""
    print("\n" + "="*80)
    print("TESTING JOB MATCHING SERVICE WITH LDA MODEL")
    print("="*80)
    
    try:
        service = JobMatchingService()
        print("✅ JobMatchingService initialized successfully")
        
        # Test with sample CV text
        sample_cv = """
        Data Scientist with machine learning expertise.
        Skills: Python, TensorFlow, PyTorch, scikit-learn, SQL, R
        Experience: Built predictive models for fraud detection
        Education: MS Statistics
        """
        
        print("\n[Test 2] Finding top job matches...")
        top_jobs = service.find_top_matches(sample_cv, top_n=5)
        
        if top_jobs is not None and len(top_jobs) > 0:
            print(f"✅ Got {len(top_jobs)} job recommendations:")
            for idx, job_info in enumerate(top_jobs, 1):
                if isinstance(job_info, dict):
                    print(f"   {idx}. {job_info.get('job_title', 'N/A')} - Score: {job_info.get('match_score', 0):.4f}")
                else:
                    print(f"   {idx}. {job_info}")
        else:
            print("❌ No matches returned")
            
    except Exception as e:
        print(f"❌ Error in JobMatchingService: {str(e)}")
        import traceback
        traceback.print_exc()


def test_model_artifacts():
    """Verify all model artifacts are in place"""
    print("\n" + "="*80)
    print("VERIFYING MODEL ARTIFACTS")
    print("="*80)
    
    import joblib
    from pathlib import Path
    
    model_dir = Path(__file__).parent / "final_model"
    
    artifacts = {
        "lda_model.joblib": "LDA Model",
        "count_vectorizer.joblib": "CountVectorizer",
        "job_topic_distributions.joblib": "Job Topic Distributions",
        "jobs_dataframe.pkl": "Jobs DataFrame (PKL)",
        "jobs_dataframe.csv": "Jobs DataFrame (CSV)"
    }
    
    all_exist = True
    for filename, description in artifacts.items():
        filepath = model_dir / filename
        exists = filepath.exists()
        status = "✅" if exists else "❌"
        size = f"({filepath.stat().st_size / 1024:.1f} KB)" if exists else ""
        print(f"{status} {description}: {filename} {size}")
        if not exists:
            all_exist = False
    
    if all_exist:
        print("\n✅ All model artifacts are present!")
    else:
        print("\n❌ Some model artifacts are missing!")
    
    return all_exist


def test_matching_quality():
    """Test the quality of matches with multiple CVs"""
    print("\n" + "="*80)
    print("TESTING MATCHING QUALITY")
    print("="*80)
    
    test_cvs = [
        {
            "name": "ML Engineer",
            "text": "Machine learning engineer with deep learning expertise. Skills: TensorFlow, PyTorch, Python, NLP, Computer Vision"
        },
        {
            "name": "DevOps Engineer", 
            "text": "DevOps engineer with cloud infrastructure experience. Skills: Kubernetes, Docker, AWS, CI/CD, Linux"
        },
        {
            "name": "Frontend Developer",
            "text": "Frontend developer specializing in React and modern web development. Skills: JavaScript, React, TypeScript, CSS, REST APIs"
        }
    ]
    
    try:
        service = CVMatchingService()
        
        for cv in test_cvs:
            print(f"\n[CV: {cv['name']}]")
            result = service.match_cv(cv['text'], top_n=3)
            
            if result and result.get('success'):
                matches = result.get('matches', [])
                if matches:
                    for i, match in enumerate(matches, 1):
                        score = match.get('similarity_score', 0) * 100
                        print(f"  {i}. {match.get('job_title')} - {score:.2f}%")
                else:
                    print("  No matches found")
            else:
                error = result.get('error') if isinstance(result, dict) else str(result)
                print(f"  Error: {error}")
                
    except Exception as e:
        print(f"❌ Error during matching quality test: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n" + "🚀 "*40)
    print("LDA MODEL API COMPREHENSIVE TEST SUITE")
    print("🚀 "*40)
    
    # Run all tests
    test_model_artifacts()
    test_cv_matching_service()
    test_matching_service()
    test_matching_quality()
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED!")
    print("="*80)
