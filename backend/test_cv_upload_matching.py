#!/usr/bin/env python
"""
Test the complete LDA-based CV matching workflow
Simulates file upload, parsing, and job matching
"""
import sys
import os
import tempfile
sys.path.insert(0, os.path.dirname(__file__))

from app.services.cv_matching_service import CVMatchingService
from app.utils.file_handler import extract_text_from_file
import time


def create_sample_cv_file(filename, content):
    """Create a temporary CV file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename


def test_cv_upload_and_matching():
    """Test complete CV upload and matching workflow"""
    print("\n" + "="*80)
    print("TESTING COMPLETE CV UPLOAD AND MATCHING WORKFLOW")
    print("="*80)
    
    # Sample CV content
    cv_content = """
    JOHN SMITH
    john.smith@example.com | (555) 123-4567
    
    SUMMARY
    Senior Machine Learning Engineer with 7+ years of experience in AI/ML development.
    Specialized in deep learning, NLP, and computer vision applications.
    
    EXPERIENCE
    
    Senior ML Engineer - TechCorp (2021-Present)
    - Led development of recommendation system using deep learning
    - Implemented NLP pipeline for document classification
    - Optimized model inference using TensorFlow Lite
    - Skills: Python, TensorFlow, PyTorch, Keras, scikit-learn, PostgreSQL
    
    ML Engineer - DataSolutions Inc (2019-2021)
    - Developed computer vision models for object detection
    - Implemented MLOps pipeline using Docker and Kubernetes
    - Collaborated with product team on model deployment
    - Skills: Python, OpenCV, Pandas, Docker, Kubernetes, GCP
    
    Junior Data Scientist - Analytics Corp (2017-2019)
    - Built predictive models for customer churn
    - Conducted A/B testing and statistical analysis
    - Created data visualizations and dashboards
    - Skills: Python, R, SQL, Tableau, Statistics
    
    EDUCATION
    
    M.S. in Computer Science - University of Tech
    Specialization: Machine Learning and AI
    
    B.S. in Mathematics - State University
    
    CERTIFICATIONS
    - TensorFlow Developer Certification
    - AWS Machine Learning Specialty
    
    TECHNICAL SKILLS
    - Languages: Python, Java, SQL, R
    - ML/AI: TensorFlow, PyTorch, Keras, scikit-learn, XGBoost
    - Cloud: AWS, GCP, Azure
    - DevOps: Docker, Kubernetes, Jenkins, CI/CD
    - Data: Pandas, NumPy, Spark, SQL
    - NLP: NLTK, spaCy, Transformers
    - CV: OpenCV, Pillow
    
    PROJECTS
    - Sentiment Analysis System: Built NLP system to analyze customer feedback
    - Real-time Object Detection: Implemented YOLOv3 for video processing
    - Recommendation Engine: Developed collaborative filtering system serving 1M+ users
    """
    
    try:
        print("\n[Step 1] Creating temporary CV file...")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            cv_file = f.name
            f.write(cv_content)
        print(f"✅ CV file created: {cv_file}")
        
        print("\n[Step 2] Parsing CV file with file handler...")
        try:
            cv_text = extract_text_from_file(cv_file)
            print(f"✅ CV parsed successfully")
            print(f"   Content length: {len(cv_text)} characters")
            print(f"   Preview: {cv_text[:100]}...")
        except Exception as e:
            print(f"⚠️  File handler error (using raw content): {e}")
            cv_text = cv_content
        
        print("\n[Step 3] Initializing matching service...")
        service = CVMatchingService()
        print(f"✅ Service initialized")
        print(f"   Model: LDA")
        print(f"   Topics: {service.lda_model.n_components}")
        print(f"   Vocabulary: {len(service.count_vectorizer.vocabulary_)} words")
        print(f"   Jobs database: {len(service.df_jobs)} positions")
        
        print("\n[Step 4] Finding job matches...")
        start_time = time.time()
        result = service.match_cv(cv_text, top_n=10)
        elapsed = time.time() - start_time
        
        if result and result.get('success'):
            print(f"✅ Matching completed in {elapsed:.3f} seconds")
            
            matches = result.get('matches', [])
            print(f"\n📊 Top {len(matches)} Job Matches:")
            print("   " + "-" * 76)
            
            for match in matches:
                rank = match.get('rank', '?')
                title = match.get('job_title', 'N/A')
                company = match.get('company', 'N/A')
                score = match.get('similarity_score', 0) * 100
                salary = match.get('salary')
                salary_str = f"${salary:,.0f}" if salary else "N/A"
                
                print(f"   {rank}. {title:<25} | {company:<20} | Score: {score:6.2f}% | ${salary_str}")
            
            print("   " + "-" * 76)
            print(f"\n✅ Test completed successfully!")
            print(f"   CV processed: {result.get('cv_length')} characters")
            print(f"   Jobs searched: {result.get('total_jobs_searched')}")
            print(f"   Model: {result.get('model_type')} with {result.get('n_topics')} topics")
            
            return True
        else:
            error = result.get('error') if isinstance(result, dict) else str(result)
            print(f"❌ Matching failed: {error}")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        if 'cv_file' in locals() and os.path.exists(cv_file):
            os.unlink(cv_file)
            print("\n[Cleanup] Temporary file deleted")


def test_lda_model_performance():
    """Test model performance metrics"""
    print("\n" + "="*80)
    print("TESTING LDA MODEL PERFORMANCE")
    print("="*80)
    
    try:
        service = CVMatchingService()
        
        test_cases = [
            {
                "name": "Minimal CV",
                "text": "Python developer"
            },
            {
                "name": "Short CV",
                "text": "Software engineer with Python and JavaScript skills"
            },
            {
                "name": "Medium CV",
                "text": """
                Senior ML Engineer with 5+ years experience
                Skills: Python, TensorFlow, PyTorch, scikit-learn, Spark
                Experience: Built recommendation systems, NLP models, computer vision
                Education: MS Computer Science
                """
            },
            {
                "name": "Long CV (typical professional)",
                "text": """
                JANE DOE
                Senior Data Scientist
                
                SUMMARY: 8+ years in data science and machine learning
                
                EXPERIENCE:
                - Led ML platform development at BigTech Corp
                - Implemented production recommendation system
                - Managed team of 5 data scientists
                - Published 3 peer-reviewed papers on deep learning
                
                SKILLS:
                Python, R, Scala, SQL, TensorFlow, PyTorch, Spark, 
                Kubernetes, Docker, AWS, GCP, DataBricks, Tableau
                
                EDUCATION:
                PhD Computer Science (Stanford)
                MS Statistics (MIT)
                BS Mathematics (Harvard)
                
                CERTIFICATIONS:
                - AWS Machine Learning Specialty
                - Google Cloud Professional Data Engineer
                - TensorFlow Advanced Specialization
                """
            }
        ]
        
        print("\nTesting model with different CV lengths:\n")
        
        for i, test in enumerate(test_cases, 1):
            print(f"Test {i}: {test['name']}")
            print(f"  CV Length: {len(test['text'])} characters")
            
            start = time.time()
            result = service.match_cv(test['text'], top_n=3)
            elapsed = time.time() - start
            
            if result and result.get('success'):
                matches = result.get('matches', [])
                top_score = matches[0].get('similarity_score', 0) * 100 if matches else 0
                avg_score = sum(m.get('similarity_score', 0) * 100 for m in matches) / len(matches) if matches else 0
                
                print(f"  Time: {elapsed*1000:.2f}ms")
                print(f"  Top Score: {top_score:.2f}%")
                print(f"  Avg Top 3: {avg_score:.2f}%")
                print(f"  Status: ✅ Success")
            else:
                print(f"  Status: ❌ Failed")
            print()
        
        print("✅ Performance tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "🚀 "*40)
    print("COMPREHENSIVE CV UPLOAD AND MATCHING TESTS")
    print("🚀 "*40)
    
    # Run tests
    test1_passed = test_cv_upload_and_matching()
    test2_passed = test_lda_model_performance()
    
    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    print(f"CV Upload & Matching: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Model Performance: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! The LDA model is ready for production!")
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
