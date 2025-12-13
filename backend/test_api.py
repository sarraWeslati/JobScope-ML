#!/usr/bin/env python
"""
Simple test script to debug JWT and file upload issues
"""
import requests
import json

# Test configuration
BASE_URL = "http://localhost:5000/api"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "password123"
TEST_NAME = "Test User"

def test_registration():
    """Test user registration"""
    print("\n" + "="*50)
    print("1. Testing Registration")
    print("="*50)
    
    payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "full_name": TEST_NAME
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        token = response.json().get('access_token')
        print(f"✅ Registration successful! Token: {token[:20]}...")
        return token
    else:
        print(f"❌ Registration failed!")
        return None

def test_login():
    """Test user login"""
    print("\n" + "="*50)
    print("2. Testing Login")
    print("="*50)
    
    payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        token = response.json().get('access_token')
        print(f"✅ Login successful! Token: {token[:20]}...")
        return token
    else:
        print(f"❌ Login failed!")
        return None

def test_health():
    """Test health endpoint"""
    print("\n" + "="*50)
    print("3. Testing Health Check")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print(f"✅ Health check passed!")
    else:
        print(f"❌ Health check failed!")

def test_cv_upload(token):
    """Test CV upload with authentication"""
    print("\n" + "="*50)
    print("4. Testing CV Upload with Token")
    print("="*50)
    
    if not token:
        print("❌ No token provided. Cannot test CV upload.")
        return
    
    # Create a test file
    test_file_content = "Python developer with 5 years experience in ML and Data Science. Skills: Python, TensorFlow, Scikit-learn, SQL, Docker"
    
    files = {'file': ('test_cv.txt', test_file_content)}
    headers = {'Authorization': f'Bearer {token}'}
    
    print(f"Sending file with token: {token[:20]}...")
    print(f"Headers: {headers}")
    
    response = requests.post(
        f"{BASE_URL}/cv/upload",
        files=files,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print(f"✅ CV upload successful!")
    else:
        print(f"❌ CV upload failed!")

def test_match():
    """Test matching without authentication"""
    print("\n" + "="*50)
    print("5. Testing Matching (No Auth)")
    print("="*50)
    
    payload = {
        "cv_text": "Python developer with Machine Learning experience in TensorFlow"
    }
    
    response = requests.post(f"{BASE_URL}/test-match", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print(f"✅ Matching test passed!")
    else:
        print(f"❌ Matching test failed!")

if __name__ == '__main__':
    print("\n🔧 Job Matching API Test Suite")
    
    test_health()
    
    test_match()
    
    token = test_registration()
    
    if not token:
        token = test_login()
    
    if token:
        test_cv_upload(token)
    
    print("\n" + "="*50)
    print("✅ Test suite complete!")
    print("="*50)
